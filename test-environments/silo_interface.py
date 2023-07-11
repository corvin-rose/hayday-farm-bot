import cv2
from matcher import Matcher

interface_img = cv2.imread('silo_interface.png', cv2.IMREAD_UNCHANGED)
silo_img = cv2.imread('../templates/interface/silo.png', cv2.IMREAD_UNCHANGED)
close_img = cv2.imread('../templates/interface/close.png', cv2.IMREAD_UNCHANGED)

m = Matcher()

silo_matches = m.match_template(silo_img, interface_img, 0.9)
close_matches = m.match_template(close_img, interface_img, 0.9)

m.mark_matches(silo_matches, interface_img, (255, 0, 0))
m.mark_matches(close_matches, interface_img, (0, 0, 255))

cv2.imshow('Result', interface_img)
cv2.waitKey()
