import cv2
from matcher import Matcher

interface_img = cv2.imread('harvest_interface.png', cv2.IMREAD_UNCHANGED)
harvest_scythe_img = cv2.imread('../templates/interface/harvest_scythe.png', cv2.IMREAD_UNCHANGED)

m = Matcher()

matches = m.match_template(harvest_scythe_img, interface_img, 0.8)
m.mark_matches(matches, interface_img, (255, 0, 0))

cv2.imshow('Result', interface_img)
cv2.waitKey()
