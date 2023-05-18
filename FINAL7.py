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
        self.k='0'
        self.s=0
    def callback(self, data):
        try:
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            msg = Header()# DO NOT DELETE THE BELOW THREE LINES!
            msg = data.header
            msg.frame_id = '0'  # default: STOP
            # sight variation
            #pts1 = np.float32([[99,44],[83,367],[559,113],[549,358]]) #pixel info of original img
            pts1 = np.float32([[80,40],[80,380],[559,40],[559,380]])
            pts2 = np.float32([[0,0],[0,479],[639,0],[639,479]]) # transmitted pixel info of tilted img   
            imgtilt = cv2.warpPerspective(image, cv2.getPerspectiveTransform(pts1, pts2), (640,480))
            imgresize = cv2.resize(imgtilt, (80, 60), interpolation=cv2.INTER_AREA)
            
            #color classification
            r,b,x=0,0,0
            for i in range(60):
                for j in range(80):
                    if (imgresize[i,j,0]+80<imgresize[i,j,1] and imgresize[i,j,2]+80<imgresize[i,j,1] and imgresize[i,j,0]+imgresize[i,j,2]<imgresize[i,j,1])or(imgresize[i,j,1]>180):
                        x+=1
                    elif imgresize[i,j,0]+80>=imgresize[i,j,1] and imgresize[i,j,0]>128: b+=1
                    elif imgresize[i,j,2]+80>=imgresize[i,j,1] and imgresize[i,j,2]>128: r+=1
                    else: x+=1
            # delay function: if 0 appears, sends frame_id * -1 for 2 frames to reduce spinning
            if max(r,b,x-500)==r:
                msg.frame_id = '-1'
                self.k='-1';self.s=0
                print('red',round(r/45),'%',msg.frame_id,self.k)
            elif max(r,b,x-500)==b:
                msg.frame_id = '+1'
                self.k='+1';self.s=0
                print('blue,',round(b/45),'%',msg.frame_id,self.k)
            else:
                msg.frame_id = '0'
                if self.s<=3:
                    self.s+=1
                    if self.k=='+1': msg.frame_id = '-1'
                    elif self.k=='-1': msg.frame_id = '+1'
                print('other',round((x-500)/45),'%',msg.frame_id,self.k)

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