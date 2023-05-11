import cv2
import numpy as np
import time

start_time = time.time() # start

img = cv2.imread('frame000008.png')
pts1 = np.float32([[99,44],[83,367],[559,113],[549,358]]) #pixel info of original img
pts2 = np.float32([[0,0],[0,59],[79,0],[79,59]]) # transmitted pixel info of tilted img
imgresize = cv2.warpPerspective(img, cv2.getPerspectiveTransform(pts1, pts2), (80,60))
#print(imgresize[:,:,0])  #print blue code of resized img

det=np.sum(imgresize[:,[4,75],0]>128)+np.sum(imgresize[[4,55],:,0]>128) #counting background efficiently(2 horizontal row + 2 vertical row)
if 140>=det:print('red,',det,'of 280')
else: print('blue,',det,'of 280')

end_time = time.time() # End 
execution_time = end_time - start_time
print('Execution time:', execution_time, 'seconds') #timing code speed