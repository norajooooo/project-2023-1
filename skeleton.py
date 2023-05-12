# !/usr/bin/env python3
import rospy
import numpy as np
import cv2
import sys
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count = 0
    def callback(self, data):
        try:
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            msg = Header()# DO NOT DELETE THE BELOW THREE LINES!
            msg = data.header
            msg.frame_id = '0'  # default: STOP
 
            # sight variation
            pts1 = np.float32([[99,44],[83,367],[559,113],[549,358]]) #pixel info of original img
            pts2 = np.float32([[0,0],[0,479],[639,0],[639,479]]) # transmitted pixel info of tilted img
            imgtilt = cv2.warpPerspective(image, cv2.getPerspectiveTransform(pts1, pts2), (640,480))
            imgresize = cv2.resize(imgtilt, (80, 60), interpolation=cv2.INTER_AREA)
            
            '''imgresize = cv2.resize(image[80:370,80:559], (80, 60), interpolation=cv2.INTER_AREA)
            if np.sum((imgresize[:,[15,64],1]<120)&(imgresize[:,[15,64],2]>110))+np.sum((imgresize[[11,48],:,1]<80)&(imgresize[[11,48],:,2]>140))>128:
                msg.frame_id = '+1'  # CCW (Blue background)'''
            #color classification
            r,b,x=0,0,0
            for i in range(60):
                for j in range(80):
                    if (imgresize[i,j,0]+60<imgresize[i,j,1] and imgresize[i,j,2]+60<imgresize[i,j,1] and imgresize[i,j,0]+imgresize[i,j,2]<imgresize[i,j,1])or(imgresize[i,j,1]>180):
                        x+=1
                    elif imgresize[i,j,0]+80>=imgresize[i,j,1] and imgresize[i,j,0]>128: b+=1
                    elif imgresize[i,j,2]+80>=imgresize[i,j,1] and imgresize[i,j,2]>128: r+=1
                    else: x+=1
            if max(r,b,x)==r:
                print('red',r,'of 4800')
                msg.frame_id = '-1'
            elif max(r,b,x)==b:
                print('blue,',b,'of 4800')
                msg.frame_id = '+1'
            else:
                print('other',x,'of 4800')
                msg.frame_id = '0'
            #elif np.sum((imgresize[:,[15,64],1]<120)&(imgresize[:,[15,64],0]>110))+np.sum((imgresize[[11,48],:,1]<80)&(imgresize[[11,48],:,0]>140))>128:
            #    msg.frame_id = '-1'  # CW (Red background)
            #else: msg.frame_id = '0'  # STOP (ELSE)
            self.count+=1
            self.color_pub.publish(msg)  # publish color_state

        except CvBridgeError as e:
            cv2.imshow('Image', image)
            cv2.waitKey(1)
            print(e)
    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    rospy.init_node('CompressedImages1', anonymous=False)
    detector = DetermineColor()
    rospy.spin()
