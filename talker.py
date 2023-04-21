#!/usr/bin/env python3
# license removed for brevity
from std_msgs.msg import String
import rospy
import subprocess
import time


def talker():
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('chatter', String, queue_size=10)
    time.sleep(0.1)
    for i in range(10):
        pub.publish("hello world")
    
    
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

