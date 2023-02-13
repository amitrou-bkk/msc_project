import cv2
import numpy as np
img = cv2.imread("/home/amitrou/msc_project/src/experiments/photo.jpg")
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sift = cv2.xfeatures2d.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()
orb = cv2.ORB_create(nfeatures=1500)

keypoints_sift, descriptors = sift.detectAndCompute(gray, None)
keypoints_surf, descriptors = surf.detectAndCompute(gray, None)
# keypoints_orb, descriptors = orb.detectAndCompute(gray, None)
print(f"keypoints_sift { [(k.pt, k.angle, k.class_id) for k in keypoints_surf]}")
# print(f"keypoints_sift {keypoints_sift}")
img_sift = cv2.drawKeypoints(gray, keypoints_sift, None)
cv2.imshow("Image_SIFT", img_sift)

img_surf = cv2.drawKeypoints(gray, keypoints_surf, None)
cv2.imshow("Image_SURF", img_surf)
cv2.waitKey(0)
cv2.destroyAllWindows()