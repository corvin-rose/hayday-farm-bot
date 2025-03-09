from time import sleep
from matcher import Matcher

import cv2
import numpy as np
import mss
import keyboard
import pyautogui as pa

pa.PAUSE = 0

# Preparation
FIELD_MATCHING_THRESHOLD = 0.7
HARVEST_MATCHING_THRESHOLD = 0.8
WHEAT_MATCHING_THRESHOLD = 0.3
WHEAT_GROWING_MATCHING_THRESHOLD = 0.7
BOAT_MATCHING_THRESHOLD = 0.7
MARKET_MATCHING_THRESHOLD = 0.6
SOLD_MATCHING_THRESHOLD = 0.6
NEW_OFFER_MATCHING_THRESHOLD = 0.6
PLANT_OFFER_MATCHING_THRESHOLD = 0.9
NEWSPAPER_MATCHING_THRESHOLD = 0.6
INSERT_BUTTON_MATCHING_THRESHOLD = 0.9
SILO_MATCHING_THRESHOLD = 0.9
CLOSE_MATCHING_THRESHOLD = 0.4

BOAT_ANCHOR = (1075, 285)
MARKET_ANCHOR = (770, 1150)

plant_img = cv2.imread('templates/plants/wheat.png', cv2.IMREAD_UNCHANGED)
plant_growing_img = cv2.imread('templates/plants/wheat_growing.png', cv2.IMREAD_UNCHANGED)
planting_interface_img = cv2.imread('templates/interface/planting_wheat.png', cv2.IMREAD_UNCHANGED)
field_img = cv2.imread('templates/environment/field.png', cv2.IMREAD_UNCHANGED)
harvesting_interface_img = cv2.imread('templates/interface/harvest_scythe.png', cv2.IMREAD_UNCHANGED)
boat_img = cv2.imread('templates/environment/boat.png', cv2.IMREAD_UNCHANGED)
market_img = cv2.imread('templates/environment/market.png', cv2.IMREAD_UNCHANGED)
sold_img = cv2.imread('templates/interface/sold.png', cv2.IMREAD_UNCHANGED)
new_offer_img = cv2.imread('templates/interface/new_offer.png', cv2.IMREAD_UNCHANGED)
plant_offer_img = cv2.imread('templates/interface/wheat_market.png', cv2.IMREAD_UNCHANGED)
newspaper_img = cv2.imread('templates/interface/newspaper.png', cv2.IMREAD_UNCHANGED)
insert_button_img = cv2.imread('templates/interface/insert_button.png', cv2.IMREAD_UNCHANGED)
silo_img = cv2.imread('templates/interface/silo.png', cv2.IMREAD_UNCHANGED)
close_img = cv2.imread('templates/interface/close.png', cv2.IMREAD_UNCHANGED)


class Bot:
    def __init__(self, logger, set_tracking_img):
        self.logger = logger
        self.set_tracking_img = set_tracking_img
        self.m = Matcher()
        self.silo_is_full = False
        self.harvested_plants = False
        self.planted_crops = 0

    def get_target(self):
        screen_dim = {
            'left': 0,
            'top': 0,
            'width': 1920,
            'height': 1080
        }
        with mss.mss() as sct:
            return np.array(sct.grab(screen_dim))
            # data = sct.grab(screen_dim)
            # bgra_data = np.frombuffer(data.bgra, dtype=np.uint8)
            # bgra_data = bgra_data.reshape((data.height, data.width, 4))
            # rgba_data = bgra_data[:, :, [2, 1, 0, 3]]
            # return np.array(rgba_data)

    def get_camera_pos(self):
        target = self.get_target()
        boat = self.m.match_template(boat_img, target, BOAT_MATCHING_THRESHOLD)
        if len(boat) > 0:
            ax, ay = BOAT_ANCHOR
            # self.logger.log("Target: BOAT_ANCHOR", ax, ay, boat[0][0], boat[0][1])
            return ax + ax - boat[0][0], ay + ay - boat[0][1]

        market = self.m.match_template(market_img, target, MARKET_MATCHING_THRESHOLD)
        if len(market) > 0:
            ax, ay = MARKET_ANCHOR
            dx, dy = ax - BOAT_ANCHOR[0], ay - BOAT_ANCHOR[1]
            # self.logger.log("Target: MARKET_ANCHOR", ax, ay, market[0][0], market[0][1])
            return ax + ax - market[0][0] - dx, ay + ay - market[0][1] - dy

        return 0, 0

    def check_fields_are_empty(self, target):
        return self.m.match_template_exists(field_img, target, FIELD_MATCHING_THRESHOLD)

    def check_plants_are_growing(self, target):
        return self.m.match_template_exists(plant_growing_img, target, WHEAT_GROWING_MATCHING_THRESHOLD)

    def check_silo_is_full(self, target):
        return len(self.m.match_template(silo_img, target, SILO_MATCHING_THRESHOLD)) > 0

    def drag_operation(self, drag_start, matches, target):
        pa.moveTo(drag_start[0], drag_start[1])
        boundary = self.m.matchs_to_boundary(matches)
        path = self.m.boundary_to_path(boundary)
        self.track_path(path, target)

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

    def combine_paths(self, p1, p2):
        result = []
        for (x, y, w, h) in p1:
            result.append([x, y, w, h])
        for (x, y, w, h) in p2:
            result.append([x, y, w, h])
        return result

    def translate_path(self, path, translation):
        result = []
        tx, ty = translation
        for (x, y, w, h) in path:
            result.append([x + tx, y + ty, w, h])
        return result

    def plant_crops(self, target):
        if self.m.match_template_exists(plant_img, target, WHEAT_MATCHING_THRESHOLD):
            self.logger.log("Found already grown plants. Harvesting them first...")
            return

        cx1, cy1 = self.get_camera_pos()
        empty_fields = self.m.match_template(field_img, target, FIELD_MATCHING_THRESHOLD)
        if len(empty_fields) == 0:
            self.logger.log("Empty fields gone, retrying...")
            return
        x = empty_fields[0][0]
        y = empty_fields[0][1]
        pa.click(x, y, clicks=2)
        sleep(2.0)

        target = self.get_target()
        cx2, cy2 = self.get_camera_pos()
        path = self.translate_path(empty_fields, (cx1 - cx2, cy1 - cy2))
        planting_interface = self.m.match_template(planting_interface_img, target, FIELD_MATCHING_THRESHOLD)
        if len(planting_interface) == 0:
            self.logger.log("Planting interface not found, retrying...")
            return
        if cx1 == 0 or cx2 == 0:
            self.logger.log("Camera anchor lost, retrying...")
            return

        drag_start = (planting_interface[0][0], planting_interface[0][1])
        self.drag_operation(drag_start, path, target)

    def harvest_plants(self, target):
        if self.check_plants_are_growing(target):
            self.logger.log("Found some plants, that are not fully grown. Waiting...")
            return

        cx1, cy1 = self.get_camera_pos()
        grown_plants = self.m.match_template(plant_img, target, WHEAT_MATCHING_THRESHOLD)
        if len(grown_plants) == 0:
            self.logger.log("Grown plants gone, retrying...")
            return
        x = grown_plants[0][0]
        y = grown_plants[0][1]
        pa.click(x, y)
        sleep(2.0)

        target = self.get_target()
        cx2, cy2 = self.get_camera_pos()
        path = self.translate_path(grown_plants, (cx1 - cx2, cy1 - cy2))
        harvesting_interface = self.m.match_template(harvesting_interface_img, target, HARVEST_MATCHING_THRESHOLD)
        if len(harvesting_interface) == 0:
            self.logger.log("Harvesting interface not found, retrying...")
            return
        if cx1 == 0 or cx2 == 0:
            self.logger.log("Camera anchor lost, retrying...")
            return

        drag_start = (harvesting_interface[0][0], harvesting_interface[0][1])
        self.drag_operation(drag_start, path, target)
        self.harvested_plants = True

    def sell_items(self, target):
        self.logger.log("Selling items...")
        # Open market
        market = self.m.match_template(market_img, target, MARKET_MATCHING_THRESHOLD)
        if len(market) == 0:
            self.logger.log("Market not found...")
            return
        sleep(0.2)
        pa.click(market[0][0] + 50, market[0][1])
        sleep(1.0)

        # Collect coins
        target = self.get_target()
        sold = self.m.match_template(sold_img, target, SOLD_MATCHING_THRESHOLD)
        self.track_matches(sold, target)
        if len(sold) > 0:
            self.logger.log("Collecting coins...")
        for s in sold:
            sleep(0.2)
            pa.click(s[0], s[1])
        sleep(1.0)

        # Create offers
        target = self.get_target()
        new_offers = self.m.match_template(new_offer_img, target, NEW_OFFER_MATCHING_THRESHOLD)
        self.track_matches(new_offers, target)
        if len(new_offers) > 0:
            self.logger.log("Inserting new offers...", len(new_offers))
        else:
            self.logger.log("No slots for offers found!")
        for offer in new_offers:
            if not self.create_offer(offer):
                break
        sleep(1.0)

        # Exit market
        close = self.m.match_template(close_img, target, CLOSE_MATCHING_THRESHOLD)
        if len(close) > 0:
            self.logger.log("Finished with selling. Closing market...")
            pa.click(close[0][0], close[0][1])

    def create_offer(self, offer):
        # Open new offer window
        pa.click(offer[0], offer[1])
        sleep(0.5)

        # Select target plant to sell
        target = self.get_target()
        plant_to_sell = self.m.match_template(plant_offer_img, target, PLANT_OFFER_MATCHING_THRESHOLD)
        self.track_matches(plant_to_sell, target)
        if len(plant_to_sell) > 0:
            pa.click(plant_to_sell[0][0], plant_to_sell[0][1])
        else:
            self.logger.log("Target plant not found... Assuming, that plants are empty")
            keyboard.send("esc")
            return False
        sleep(0.5)

        # Check if newspaper insert is available
        newspaper = self.m.match_template(newspaper_img, target, NEWSPAPER_MATCHING_THRESHOLD)
        self.track_matches(newspaper, target)
        if len(newspaper) > 0:
            self.logger.log("Insert to newspaper available. Inserting...")
            pa.click(newspaper[0][0], newspaper[0][1])
        sleep(0.2)

        # Insert offer
        target = self.get_target()
        insert_button = self.m.match_template(insert_button_img, target, INSERT_BUTTON_MATCHING_THRESHOLD)
        self.track_matches(insert_button, target)
        if len(insert_button) > 0:
            pa.click(insert_button[0][0], insert_button[0][1])
        else:
            self.logger.log("Insert button not found. This is a critical error, because no plants can be sold.")
            return False
        sleep(0.2)
        return True

    def check_unexpected_behaviour(self, target):
        close = self.m.match_template(close_img, target, CLOSE_MATCHING_THRESHOLD)
        if len(close) > 0:
            self.logger.log("Detected unexpected behaviour. Closing window...")
            sleep(0.2)
            pa.click(close[0][0], close[0][1])

    def track_matches(self, matches, target):
        tracked = target.copy()
        self.m.mark_matches(matches, tracked, (255, 0, 0))
        self.set_tracking_img(tracked)

    def track_path(self, path, target):
        tracked = target.copy()
        self.m.mark_path(path, tracked)
        self.set_tracking_img(tracked)

    def bot_loop(self):
        while True:
            screen = self.get_target()

            self.logger.log("Camera:", self.get_camera_pos())

            # Plant
            empty_fields = self.m.match_template(field_img, screen, FIELD_MATCHING_THRESHOLD)
            self.track_matches(empty_fields, screen)
            if len(empty_fields) > 0:
                self.logger.log("Found %d empty fields... starting planting" % (len(empty_fields)))
                self.plant_crops(screen)
                self.planted_crops += len(empty_fields)

            # Sell
            if self.harvested_plants or self.silo_is_full:
                self.silo_is_full = False
                self.sell_items(screen)
            self.harvested_plants = False

            # Harvest
            grown_plants = self.m.match_template(plant_img, screen, WHEAT_MATCHING_THRESHOLD)
            self.track_matches(grown_plants, screen)
            if not self.silo_is_full:
                if len(grown_plants) > 0:
                    self.logger.log("Found %d grown plants, starting harvesting..." % (len(grown_plants)))
                    self.harvest_plants(screen)
                else:
                    self.logger.log("No grown plants found, waiting for growing...")
                    for i in range(10):
                        if keyboard.is_pressed('q'): break
                        sleep(1.0)

            # Check Silo
            screen = self.get_target()
            if self.check_silo_is_full(screen):
                self.logger.log("Silo is full detected")
                self.silo_is_full = True

            self.check_unexpected_behaviour(screen)

            sleep(3.0)
            if keyboard.is_pressed('q'):
                self.logger.log("Stopping...")
                break
