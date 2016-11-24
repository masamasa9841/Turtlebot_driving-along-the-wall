#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from kobuki_msgs.msg import BumperEvent
precure = 0
kp = -3.7
x = 0.6
def bumper(bumper):
    global x
    x = 0
def callback(msg):
    global precure
    precure = msg.data
rospy.init_node('vel_publisher')
pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
sub = rospy.Subscriber('kinect', Float64, callback)
sob = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, bumper)
try:
    while not rospy.is_shutdown():
        vel = Twist()
        e = 0.3 - precure
        if x==0:
            vel.linear.x = x
            vel.angular.z = -0.7
            pub.publish(vel)
            time.sleep(1.0)
            x = 0.6
        else:
            vel.linear.x = x
            if 5.0<e*kp:
                vel.angular.z = 5.0
            else:
                vel.angular.z = kp*e
        pub.publish(vel)
        rospy.sleep(0.01)
except:
    pass
