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
        self.sub = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.bumper)
        self.sub1 = rospy.Subscriber('/scan', LaserScan, self.laser)
        self.vel = Twist()
        self.RESTRICTION = -0.8
        self.TARGET = 0.8
        self.SPEED = 0.4
        self.b = 3
        self.s = 0
        self.l = 0

    def bumper(self, bumper):
        #0:left 1:center 2:right
        self.b = bumper.bumper
        self.s = bumper.state

    def laser(self, laser):
        self.m = len(laser.ranges) - 1
        while math.isnan(laser.ranges[self.m]) == True and  self.m > len(laser.ranges) - 60:
            self.m -= 1
        if math.isnan(laser.ranges[self.m]) == True:
            self.l = 0
        else:
            self.l = laser.ranges[self.m]

    def run (self):
        while not rospy.is_shutdown():
            self.vel.linear.x = self.SPEED
            e = self.TARGET - self.l
            p = -e * 1.0
            print p

            self.vel.angular.z = p
            self.pub.publish(self.vel)
            rospy.sleep (0.1)

if __name__ == '__main__':
    rospy.init_node('vel_publisher')
    datw = driving_along_the_wall()
    try:
        datw.run()
    except rospy.ROSInterruptException:
        pass
