from time import sleep
from matcher import Matcher

import cv2
import numpy as np
import mss
import keyboard
import pyautogui as pa

sct = mss.mss()
pa.PAUSE = 0

# Preparation
FIELD_MATCHING_THRESHOLD = 0.7
HARVEST_MATCHING_THRESHOLD = 0.8
WHEAT_MATCHING_THRESHOLD = 0.3
BOAT_MATCHING_THRESHOLD = 0.7
MARKET_MATCHING_THRESHOLD = 0.5
SILO_MATCHING_THRESHOLD = 0.9

BOAT_ANCHOR = (1075, 285)
MARKET_ANCHOR = (825, 1150)

m = Matcher()
screen_dim = {
    'left': 0,
    'top': 0,
    'width': 1920,
    'height': 1080
}
plant_img = cv2.imread('templates/plants/wheat.png', cv2.IMREAD_UNCHANGED)
planting_interface_img = cv2.imread('templates/interface/planting_wheat.png', cv2.IMREAD_UNCHANGED)
field_img = cv2.imread('templates/environment/field.png', cv2.IMREAD_UNCHANGED)
harvesting_interface_img = cv2.imread('templates/interface/harvest_scythe.png', cv2.IMREAD_UNCHANGED)
boat_img = cv2.imread('templates/environment/boat.png', cv2.IMREAD_UNCHANGED)
market_img = cv2.imread('templates/environment/market.png', cv2.IMREAD_UNCHANGED)
silo_img = cv2.imread('templates/interface/silo.png', cv2.IMREAD_UNCHANGED)


def get_target():
    return np.array(sct.grab(screen_dim))


def get_camera_pos():
    target = get_target()
    boat = m.match_template(boat_img, target, BOAT_MATCHING_THRESHOLD)
    if len(boat) > 0:
        ax, ay = BOAT_ANCHOR
        # print("Target: BOAT_ANCHOR", ax, ay, boat[0][0], boat[0][1])
        return ax + ax - boat[0][0], ay + ay - boat[0][1]

    market = m.match_template(market_img, target, MARKET_MATCHING_THRESHOLD)
    if len(market) > 0:
        ax, ay = MARKET_ANCHOR
        dx, dy = ax - BOAT_ANCHOR[0], ay - BOAT_ANCHOR[1]
        # print("Target: MARKET_ANCHOR", ax, ay, market[0][0], market[0][1])
        return ax + ax - market[0][0] - dx, ay + ay - market[0][1] - dy

    return 0, 0


def check_fields_are_empty(target):
    return m.match_template_exists(field_img, target, FIELD_MATCHING_THRESHOLD)


def check_silo_is_full(target):
    return len(m.match_template(silo_img, target, SILO_MATCHING_THRESHOLD)) > 0


def drag_operation(drag_start, matches):
    pa.moveTo(drag_start[0], drag_start[1])
    boundary = m.matchs_to_boundary(matches)
    path = m.boundary_to_path(boundary)

    pa.mouseDown(button='left')
    pa.moveTo(path[0][0], path[0][1], duration=0.2)
    sleep(0.2)
    for (x, y) in path:
        if keyboard.is_pressed('q'):
            return
        pa.moveTo(x, y, duration=0.75, _pause=False)
        sleep(0.75)
    last_pt = path[len(path)-1]
    pa.moveTo(last_pt[0] + 50, last_pt[1] + 50)
    pa.mouseUp()

def combine_paths(p1, p2):
    result = []
    for (x, y, w, h) in p1:
        result.append([x, y, w, h])
    for (x, y, w, h) in p2:
        result.append([x, y, w, h])
    return result


def translate_path(path, translation):
    result = []
    tx, ty = translation
    for (x, y, w, h) in path:
        result.append([x + tx, y + ty, w, h])
    return result


def plant_crops(target):
    cx1, cy1 = get_camera_pos()
    empty_fields = m.match_template(field_img, target, FIELD_MATCHING_THRESHOLD)
    if len(empty_fields) == 0:
        print("Empty fields gone, retrying...")
        return
    x = empty_fields[0][0]
    y = empty_fields[0][1]
    pa.click(x, y, clicks=2)
    sleep(2.0)

    target = get_target()
    cx2, cy2 = get_camera_pos()
    path = translate_path(empty_fields, (cx1 - cx2, cy1 - cy2))
    planting_interface = m.match_template(planting_interface_img, target, FIELD_MATCHING_THRESHOLD)
    if len(planting_interface) == 0:
        print("Planting interface not found, retrying...")
        return
    if cx1 == 0 or cx2 == 0:
        print("Camera anchor lost, retrying...")
        return

    drag_start = (planting_interface[0][0], planting_interface[0][1])
    drag_operation(drag_start, path)


def harvest_plants(target):
    cx1, cy1 = get_camera_pos()
    grown_plants = m.match_template(plant_img, target, WHEAT_MATCHING_THRESHOLD)
    if len(grown_plants) == 0:
        print("Grown plants gone, retrying...")
        return
    x = grown_plants[0][0]
    y = grown_plants[0][1]
    pa.click(x, y)
    sleep(2.0)

    target = get_target()
    cx2, cy2 = get_camera_pos()
    path = translate_path(grown_plants, (cx1 - cx2, cy1 - cy2))
    harvesting_interface = m.match_template(harvesting_interface_img, target, HARVEST_MATCHING_THRESHOLD)
    if len(harvesting_interface) == 0:
        print("Harvesting interface not found, retrying...")
        return
    if cx1 == 0 or cx2 == 0:
        print("Camera anchor lost, retrying...")
        return

    drag_start = (harvesting_interface[0][0], harvesting_interface[0][1])
    drag_operation(drag_start, path)


# Start of Program
print("=====================================================================")
print("  _  _             ___              ___                 ___      _   ")
print(" | || |__ _ _  _  |   \ __ _ _  _  | __|_ _ _ _ _ __   | _ ) ___| |_ ")
print(" | __ / _` | || | | |) / _` | || | | _/ _` | '_| '  \  | _ \/ _ \  _|")
print(" |_||_\__,_|\_, | |___/\__,_|\_, | |_|\__,_|_| |_|_|_| |___/\___/\__|")
print("            |__/             |__/                                    ")
print()
print("=====================================================================")
print("Press 's' to start")
print("Once started press 'q' to stop")
print()
keyboard.wait('s')

print()
while True:
    screen = get_target()

    print("Camera:", get_camera_pos())

    empty_fields = m.match_template(field_img, screen, FIELD_MATCHING_THRESHOLD)
    if len(empty_fields) > 0:
        print("Found %d empty fields... starting planting" % (len(empty_fields)))
        plant_crops(screen)

    grown_plants = m.match_template(plant_img, screen, WHEAT_MATCHING_THRESHOLD)
    if len(grown_plants) > 0:
        print("Found %d grown plants, starting harvesting..." % (len(grown_plants)))
        harvest_plants(screen)
    else:
        print("No grown plants found, waiting for growing...")
        sleep(30)

    if check_silo_is_full(screen):
        print("Silo is full. TODO: sell items")
        break

    sleep(1.0)
    if keyboard.is_pressed('q'):
        print("Stopping...")
        # TODO: print stats
        break
