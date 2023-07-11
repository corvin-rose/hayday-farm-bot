import cv2
from matcher import Matcher

boat_env_img = cv2.imread('boat_pos.png', cv2.IMREAD_UNCHANGED)
boat_env_2_img = cv2.imread('boat_pos_2.png', cv2.IMREAD_UNCHANGED)
boat_img = cv2.imread('../templates/environment/boat.png', cv2.IMREAD_UNCHANGED)
market_img = cv2.imread('../templates/environment/market.png', cv2.IMREAD_UNCHANGED)

m = Matcher()

boat = m.match_template(boat_img, boat_env_img)
m.mark_matches(boat, boat_env_img, (255, 0, 0))

print("Boat", boat[0][0], boat[0][1])
cv2.imshow('Result', boat_env_img)
cv2.waitKey()

boat_2 = m.match_template(boat_img, boat_env_2_img)
market = m.match_template(market_img, boat_env_2_img)
m.mark_matches(boat_2, boat_env_2_img, (255, 0, 0))
m.mark_matches(market, boat_env_2_img, (255, 0, 0))

print("Market", boat[0][0] + market[0][0] - boat_2[0][0], boat[0][1] + market[0][1] - boat_2[0][1])
cv2.imshow('Result', boat_env_2_img)
cv2.waitKey()
