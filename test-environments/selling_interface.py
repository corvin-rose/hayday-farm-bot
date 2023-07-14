import cv2
import mss
from matcher import Matcher

sct = mss.mss()

interface_img = cv2.imread('selling_interface.png', cv2.IMREAD_UNCHANGED)
plant_offer_img = cv2.imread('../templates/interface/wheat_market.png', cv2.IMREAD_UNCHANGED)
newspaper_img = cv2.imread('../templates/interface/newspaper.png', cv2.IMREAD_UNCHANGED)
insert_button_img = cv2.imread('../templates/interface/insert_button.png', cv2.IMREAD_UNCHANGED)

m = Matcher()

plant_offer_matches = m.match_template(plant_offer_img, interface_img, 0.9)
newspaper_img_matches = m.match_template(newspaper_img, interface_img, 0.6)
insert_button_matches = m.match_template(insert_button_img, interface_img, 0.9)

m.mark_matches(plant_offer_matches, interface_img, (255, 0, 0))
m.mark_matches(newspaper_img_matches, interface_img, (255, 255, 0))
m.mark_matches(insert_button_matches, interface_img, (0, 255, 255))

cv2.imshow('Result', interface_img)
cv2.waitKey()
