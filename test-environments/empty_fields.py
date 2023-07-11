import cv2
from matcher import Matcher

farm_img = cv2.imread('empty_fields.png', cv2.IMREAD_UNCHANGED)
field_img = cv2.imread('../templates/environment/field.png', cv2.IMREAD_UNCHANGED)

m = Matcher()

field_matches = m.match_template(field_img, farm_img, 0.7)
m.mark_matches(field_matches, farm_img, (255, 255, 0))

cv2.imshow('Result', farm_img)
cv2.waitKey()
