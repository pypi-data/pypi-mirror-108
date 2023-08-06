import pytesseract
import numpy as np
import cv2 as cv
import sys
import re

_TP_THRESH = [(57, 200, 200), (60, 255, 255)]
_ST_THRESH = [(0, 200, 200),  (3, 255, 255)]
_BL_THRESH = [(102, 180, 180), (108, 255, 255)]
_AV_THRESH = [(145, 200, 200), (153, 255, 255)]


def find_price_points(original, crange, invert=False, debug=False):
    image = cv.cvtColor(original.copy(), cv.COLOR_BGR2HSV)
    thresh = cv.inRange(image, *crange)
    contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[-2]

    values = []
    for index, contour in enumerate(contours):
        x, y, w, h = cv.boundingRect(contour)
        perimeter = w * 2 + h * 2
        
        if perimeter < 100:
            continue

        roi = original[y:y + h, x:x + w]
        roi = cv.resize(roi, None, fx=5.0, fy=5.0, interpolation=cv.INTER_CUBIC)
        roi = cv.bilateralFilter(roi, 32, 10, 10)
        roi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
        if invert:
            roi = 255 - roi
        roi = cv.fastNlMeansDenoising(roi, 14, 21, 5)
        if debug:
            cv.imwrite(f"roi_{x}_{y}.jpg", roi)

        text = pytesseract.image_to_string(roi, config='--psm 6 --oem 3 outputbase digits')
        for line in text.splitlines():
            try:
                value = float(re.sub("[^\d\.]", "", line))
            except ValueError:
                continue
            values.append(value)

    return values

def get_change(current, previous):
    if current == previous:
        return 0.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')

def get_change_val(current, change):
    return current * ((change / 100.0) + 1)

def parse_signal_image(image_data, st_tol=20, tp_tol=150, bl_tol=20):
    file_bytes = np.asarray(image_data, dtype=np.uint8)
    image = cv.imdecode(file_bytes, cv.IMREAD_COLOR)

    points = {
        "tp": find_price_points(image, _TP_THRESH),
        "st": find_price_points(image, _ST_THRESH, True),
        "bl": find_price_points(image, _BL_THRESH, True),
        "av": find_price_points(image, _AV_THRESH, True)
    }
    
    direction = "unknown"
    points.update({"direction": direction})

    max_st = max(points['st'])
    min_st = min(points['st'])

    # Current setup
    if len(points['av']):
        av = sum(points['av']) / len(points['av'])
    else:
        av = 0.0

    # Delayed setup
    if len(points['bl']) == 2:
        bl_av = sum(points['bl']) / len(points['bl'])
    else:
        bl_av = 0.0

    if get_change(av, np.median(points['tp'])) < tp_tol:
        av = av
    elif get_change(bl_av, np.median(points['tp'])) < tp_tol:
        av = bl_av
        points['av'] = [bl_av]
    else:
        return points

    # All TPs, BLs and AV are greater than highest stop, long
    if all(i > max_st for i in points['tp'] + points['bl'] + points['av']):
        direction = "long"
    # All TPs, BLs and AV are lower than lowest stop, short
    elif all(i < min_st for i in points['tp'] + points['bl'] + points['av']):
        direction = "short"

    points.update({"direction": direction})

    if direction  == "long":
        points['tp'] = list(set(map(lambda p: p if get_change(p, av) <= tp_tol else get_change_val(av, tp_tol), points['tp'])))
        points['st'] = list(set(map(lambda p: p if get_change(p, av) <= st_tol else get_change_val(av, -st_tol), points['st'])))
        points['bl'] = list(set(map(lambda p: p if get_change(p, av) <= bl_tol else get_change_val(av, -bl_tol), points['bl'])))
    elif direction == "short":
        points['st'] = list(set(map(lambda p: p if get_change(p, av) <= st_tol else get_change_val(av, st_tol), points['st'])))
        points['bl'] = list(set(map(lambda p: p if get_change(p, av) <= bl_tol else get_change_val(av, bl_tol), points['bl'])))

    points['tp'] = sorted(points['tp'])
    points['st'] = sorted(points['st'])
    points['bl'] = sorted(points['bl'])

    return points

__all__ = ['parse_signal_image']

