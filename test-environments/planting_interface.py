import cv2
from matcher import Matcher

interface_img = cv2.imread('planting_interface.png', cv2.IMREAD_UNCHANGED)
plant_interface_img = cv2.imread('../templates/interface/planting_wheat.png', cv2.IMREAD_UNCHANGED)

m = Matcher()

matches = m.match_template(plant_interface_img, interface_img, 0.7)
m.mark_matches(matches, interface_img, (255, 0, 0))

cv2.imshow('Result', interface_img)
cv2.waitKey()
