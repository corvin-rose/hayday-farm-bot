import cv2
from matcher import Matcher

farm_img = cv2.imread('farm_market.png', cv2.IMREAD_UNCHANGED)
market_img = cv2.imread('../templates/environment/market.png', cv2.IMREAD_UNCHANGED)

m = Matcher()

matches = m.match_template(market_img, farm_img, 0.5)
m.mark_matches(matches, farm_img, (255, 255, 0))

cv2.imshow('Result', farm_img)
cv2.waitKey()
