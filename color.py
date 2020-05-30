# import cv2
# import cartoon
#
# def funcBrightContrast(bright=0):
#     bright = cv2.getTrackbarPos('bright', 'Life2Coding')
#     contrast = cv2.getTrackbarPos('contrast', 'Life2Coding')
#
#     effect = apply_brightness_contrast(img, bright, contrast)
#     height, width = effect.shape[:2]
#     cv2.namedWindow('Effect', cv2.WINDOW_NORMAL)
#     cv2.resizeWindow('Effect', width, height)
#     cv2.imshow('Effect', effect)
#
#
# def apply_brightness_contrast(input_img, brightness=255, contrast=127):
#     brightness = map(brightness, 0, 510, -255, 255)
#     contrast = map(contrast, 0, 254, -127, 127)
#
#     if brightness != 0:
#         if brightness > 0:
#             shadow = brightness
#             highlight = 255
#         else:
#             shadow = 0
#             highlight = 255 + brightness
#         alpha_b = (highlight - shadow) / 255
#         gamma_b = shadow
#
#         buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
#     else:
#         buf = input_img.copy()
#
#     if contrast != 0:
#         f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
#         alpha_c = f
#         gamma_c = 127 * (1 - f)
#
#         buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
#
#     cv2.putText(buf, 'B:{},C:{}'.format(brightness, contrast), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#     return buf
#
#
# def map(x, in_min, in_max, out_min, out_max):
#     return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
#
#
# if __name__ == '__main__':
#     original = cv2.imread("sp.jpg", 1)
#     img = cartoon.cartoon
#     height, width = img.shape[:2]
#
#     cv2.namedWindow('Life2Coding', cv2.WINDOW_NORMAL)
#     cv2.resizeWindow('Life2Coding', width, height)
#
#     bright = 255
#     contrast = 127
#
#     # Brightness value range -255 to 255
#     # Contrast value range -127 to 127
#
#     cv2.createTrackbar('bright', 'Life2Coding', bright, 2 * 255, funcBrightContrast)
#     cv2.createTrackbar('contrast', 'Life2Coding', contrast, 2 * 127, funcBrightContrast)
#     funcBrightContrast(0)
#     cv2.imshow('Life2Coding', original)
#
# cv2.waitKey(0)



