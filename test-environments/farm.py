import cv2
from matcher import Matcher

farm_img = cv2.imread('farm.png', cv2.IMREAD_UNCHANGED)
plant_img = cv2.imread('../templates/plants/wheat.png', cv2.IMREAD_UNCHANGED)
plant_growing_img = cv2.imread('../templates/plants/wheat_growing.png', cv2.IMREAD_UNCHANGED)
field_img = cv2.imread('../templates/environment/field.png', cv2.IMREAD_UNCHANGED)

m = Matcher()

plant_matches = m.match_template(plant_img, farm_img, 0.3)
plant_growing_matches = m.match_template(plant_growing_img, farm_img, 0.7)
field_matches = m.match_template(field_img, farm_img)

boundary = m.matchs_to_boundary(plant_matches)
path = m.boundary_to_path(boundary)
m.mark_boundary(boundary, farm_img)
m.mark_path(path, farm_img)

m.mark_matches(plant_matches, farm_img, (255, 0, 0))
m.mark_matches(plant_growing_matches, farm_img, (255, 0, 0))
m.mark_matches(field_matches, farm_img, (255, 255, 0))


cv2.imshow('Result', farm_img)
cv2.waitKey()
