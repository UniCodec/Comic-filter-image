import cv2
import numpy as np

img = cv2.imread('im.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
b_img = cv2.medianBlur(gray, 7)

low_sigma = cv2.GaussianBlur(b_img, (3, 3), 0)
high_sigma = cv2.GaussianBlur(b_img, (15, 15), 0)
# Calculate the DoG by subtracting
dog = low_sigma - high_sigma
dog = cv2.fastNlMeansDenoising(dog, None, 70, 7, 21)

edges = cv2.Canny(b_img, 45, 7)
edges = cv2.fastNlMeansDenoising(edges, None, 50, 7, 21)
final_edges = cv2.addWeighted(dog, 1, edges, 1, 0)

ret, final_edges = cv2.threshold(final_edges, 127, 255, cv2.THRESH_BINARY_INV)

# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
# final_edges = cv2.erode(final_edges, kernel, iterations=1)

# 2) Color
color = cv2.bilateralFilter(img, 9, 300, 300)
b, g, r = cv2.split(color)
b = cv2.medianBlur(b, 5)
g = cv2.medianBlur(g, 5)
r = cv2.medianBlur(r, 5)
color = cv2.merge((b, g, r))

Z = color.reshape((-1, 3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 8
ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
color = res.reshape((color.shape))

color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
# multiple by a factor to change the saturation
color[..., 1] = color[..., 1]*1.5
# decreasing the V channel by a factor from the original
# color[..., 2] = color[..., 2]*1
color = cv2.cvtColor(color, cv2.COLOR_HSV2BGR)

# 3) Cartoon
cartoon = cv2.bitwise_and(color, color, mask=final_edges)

# display all Images
height, width = img.shape[:2]
cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Original Image', width, height)
cv2.imshow('Original Image', img)

height, width = final_edges.shape[:2]
cv2.namedWindow('Edges', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Edges', width, height)
cv2.imshow('Edges', final_edges)

height, width = color.shape[:2]
cv2.namedWindow('Color', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Color', width, height)
cv2.imshow('Color', color)

height, width = cartoon.shape[:2]
cv2.namedWindow('Cartoon Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Cartoon Image', width, height)
cv2.imshow('Cartoon Image', cartoon)

cv2.waitKey(0)
cv2.destroyAllWindows()
