import numpy as np
import cv2
import sys
for k in range(1,16):
    image = cv2.imread("C:/Users/scien/Desktop/frames/"+str(k)+".png")
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    imgresize = cv2.resize(image[80:370,80:559], (80, 60), interpolation=cv2.INTER_AREA)
   # cv2.imshow('color_image',imgresize)
   # print(image[20][20])
    image_deter=imgresize.reshape((-1,3))
#    image_deter=np.concatenate((imgresize[:,[15,64]].reshape((-1,3)),imgresize[[11,48],:].reshape((-1,3))),axis=0)      #convert to 1-D array(except color channel)
    to_np=lambda x:np.array(x)
    color_dict={"red":(255,0,0),"blue":(0,0,255),"black":(0,0,0),"white":(255,255,255),"yellow":(255,255,0),"green":(0,255,0),"purple":(255,0,255),"blue_green":(0,255,255)}
    color_count={}           
    for key in color_dict:
        color_dict[key]=to_np(color_dict[key])
        color_count[key]=0
    
    pixel_count=image_deter.shape[0]
    for i in range(pixel_count):
        current_pixel=image_deter[i]
        global current_col
        current_col=None
        dist_min=float("inf")
        for key in color_dict:
            if np.abs(color_dict[key]-current_pixel).sum()<dist_min:
                current_col=key
                dist_min=np.abs(color_dict[key]-current_pixel).sum()
        color_count[current_col]+=1
    max_list=[0,None]
    for key in color_count:
        if color_count[key]>max_list[0]:
            max_list[0]=color_count[key]
            max_list[1]=key

    if max_list[1]=="red": frame_id = '-1' # CW (Red background)
    elif max_list[1]=="blue": frame_id = '+1' # CCW (Blue background)
    elif max_list[1]=="blue_green":frame_id="+1"
    elif max_list[1]=="yellow" :frame_id="-1"
    else: frame_id=0 
    print(frame_id)