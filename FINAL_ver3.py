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
        #self.pts1 = np.float32([[99,44],[83,367],[559,113],[549,358]]) # pre-round monitor 4 vertex position
        #self.pts2 = np.float32([[0,0],[0,479],[639,0],[639,479]]) # converted position

    def callback(self, data):
        try:
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            msg = Header()# DO NOT DELETE THE BELOW THREE LINES!
            msg = data.header
            msg.frame_id = '0'  # default: STOP

            # determine background color
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)   #to RGB
            imgresize = cv2.resize(image[80:370,80:559], (80, 60), interpolation=cv2.INTER_AREA)
            image_deter=np.concatenate((imgresize[:,[15,64]].reshape((-1,3)),imgresize[[11,48],:].reshape((-1,3))),axis=0)      #convert to 1-D array(except color channel)
            color_count={"red":0,"blue":0,"etc":0}

            
            pixel_count=image_deter.shape[0]
            for i in range(pixel_count):
                cup=image_deter[i]
                X=cup[0]/cup.sum()
                Y=cup[1]/cup.sum()
                if Y>=0.6*(X-0.18) and Y<=4(X-0.25):
                    color_count["red"]+=1
                elif Y>=4(X-0.25) and Y<=0.45-0.25*X:
                    color_count["blue"]+=1
                else:
                    color_count["etc"]+=1
            max_list=[0,None]
            for key in color_count:
                if color_count[key]>max_list[0]:
                    max_list[0]=color_count[key]
                    max_list[1]=key
            if max_list[1]=="red": msg.frame_id = '-1' # CW (Red background)
            elif max_list[1]=="blue": msg.frame_id = '+1' # CCW (Blue background)
            else: msg.frame_id="0"
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