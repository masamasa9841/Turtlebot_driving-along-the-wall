#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent

class driving_along_the_wall(object):
    def __init__(self):
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
        self.sub3 = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.bumper)
        self.vel = Twist()
        self.speed = 0.7
        self.b = 3
        self.s = 0


    def bumper(self, bumper):
        #0:left 1:center 2:right
        self.b = bumper.bumper
        self.s = bumper.state

    def run (self):
        while not rospy.is_shutdown():
            print self.b,self.s
            self.vel.linear.x = 0.15
            if (self.b == 0 or self.b == 1) and self.s == 1:
                self.vel.angular.z = -0.8
            else:
                self.vel.angular.z = 0.8
            self.pub.publish(self.vel)
            rospy.sleep(0.1)

if __name__ == '__main__':
    rospy.init_node('vel_publisher')
    datw = driving_along_the_wall()
    try:
        datw.run()
    except rospy.ROSInterruptException:
        pass
