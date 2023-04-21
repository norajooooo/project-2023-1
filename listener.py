#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " I heard %s", data)
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()


