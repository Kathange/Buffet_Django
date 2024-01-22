from PIL import Image
import numpy as np
import cv2 as cv

answer = Image.open("confusion/image_16_0.png").convert('L')
predict = Image.open("confusion/total_mask.png").convert('L')
mask_width, mask_height = answer.size

total = mask_width * mask_height

fp = 0
fn = 0
tp = 0
tn = 0

value = 98
value2 = 128

box_img = np.zeros((mask_height,mask_width,3), np.uint8)




for y in range(mask_width):
    for x in range(mask_height):
        if ((answer.getpixel((y,x)) == value2)&(predict.getpixel((y,x)) == value) ):
            tp +=1
            box_img[x][y] = (255 , 0, 0)
        if ((answer.getpixel((y,x)) != value2)&(predict.getpixel((y,x)) == value) ):
            fn +=1
            box_img[x][y] = (0 , 255, 0)
        if ((answer.getpixel((y,x)) == value2)&(predict.getpixel((y,x)) != value) ):
            fp +=1
            box_img[x][y] = (0 , 0, 255)
        if ((answer.getpixel((y,x)) != value2)&(predict.getpixel((y,x)) != value) ):
            tn +=1
            box_img[x][y] = (255 , 255, 0)


tp = tp / total
fp = fp / total
fn = fn / total
tn = tn / total

cv.imshow("img", box_img)
print("tp:", tp)
print(f"fp: {fp:.8f}")
print(f"fn: {fn:.8f}")
print("tn:", tn)


cv.waitKey(0)

#由灰度圖來辨別食物的位置



