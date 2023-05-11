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
            imgresize = cv2.resize(image[80:370,80:559], (80, 60), interpolation=cv2.INTER_AREA)
            det=np.sum(imgresize[:,[15,64],0]>128)+np.sum(imgresize[[11,48],:,0]>128) # counting background efficiently (2 horizontal row + 2 vertical row)
            if 140>=det: msg.frame_id = '-1' # CW (Red background)
            else: msg.frame_id = '+1' # CCW (Blue background)
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
