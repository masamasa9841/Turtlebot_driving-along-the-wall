#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from sensor_msgs.msg import LaserScan
import math

class driving_along_the_wall(object):
    def __init__(self):
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
        self.sub1 = rospy.Subscriber('/scan', LaserScan, self.laser)
        self.vel = Twist()
        self.RESTRICTION = -0.8
        self.TARGET = 1.0
        self.SPEED = 1.0
        self.l = 0

    def laser(self, laser):
        self.m = 0
        while math.isnan(laser.ranges[self.m]) == True and self.m < 30:
            self.m += 1
        if math.isnan(laser.ranges[self.m]) == True:
            self.vel.linear.x = self.SPEED / 2.0
            self.vel.angular.z = -0.5
        else:
            self.vel.linear.x = self.SPEED
            self.l = laser.ranges[self.m]
            e = self.TARGET - self.l
            p = e * 1.5
            self.vel.angular.z = p
        self.pub.publish(self.vel)

if __name__ == '__main__':
    rospy.init_node('vel_publisher')
    datw = driving_along_the_wall()
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
