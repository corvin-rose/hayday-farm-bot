import cv2
from matcher import Matcher

interface_img = cv2.imread('market_interface.png', cv2.IMREAD_UNCHANGED)
sold_img = cv2.imread('../templates/interface/sold.png', cv2.IMREAD_UNCHANGED)
new_offer_img = cv2.imread('../templates/interface/new_offer.png', cv2.IMREAD_UNCHANGED)
close_img = cv2.imread('../templates/interface/close.png', cv2.IMREAD_UNCHANGED)

m = Matcher()

sold_matches = m.match_template(sold_img, interface_img, 0.9)
new_offer_matches = m.match_template(new_offer_img, interface_img, 0.9)
close_matches = m.match_template(close_img, interface_img, 0.4)

m.mark_matches(sold_matches, interface_img, (255, 0, 0))
m.mark_matches(new_offer_matches, interface_img, (0, 255, 0))
m.mark_matches(close_matches, interface_img, (0, 0, 255))

cv2.imshow('Result', interface_img)
cv2.waitKey()
