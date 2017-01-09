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
        self.SPEED = 0.2
        self.b = 3
        self.s = 0
        self.l = 0
        self.ss = 2
        self.count = 0
        self.count2 = 0
        self.up=[]

    def bumper(self, bumper):
        #0:left 1:center 2:right
        self.b = bumper.bumper
        self.s = bumper.state

    def laser(self, laser):
        i=340
        while math.isnan(laser.ranges[i]) == True and i>len(laser.ranges)-200:
            i -=1
        if math.isnan(laser.ranges[i]) == True:
            self.ss = 2
        else:
            self.ss = laser.ranges[i]

        self.m = len(laser.ranges) - 1
        while math.isnan(laser.ranges[self.m]) == True and  self.m > len(laser.ranges) - 30:
            self.m -= 1
        if math.isnan(laser.ranges[self.m]) == True:
            self.l = 0
        else:
            self.l = laser.ranges[self.m]

    def run (self):
        while not rospy.is_shutdown():
            if self.ss <= 0.6:
                self.vel.angular.z = -3
                self.vel.linear.x = 0
                print 1
            else:
                if self.b==1:
                    self.vel.angular.z = -1
                    self.vel.linear.x = 0
                else:
                    self.vel.linear.x = self.SPEED
                    e = self.TARGET - self.l
                    p = -e * 1.0
                    print 2
                    if math.fabs(p) >= 2:
                        e = self.TARGET - self.up[0]
                        p = -e
                        if math.fabs(p) >= 2:
                            p = -2
            self.vel.angular.z = p
            while self.count <= 41:
                self.up.append(8)
                self.count = self.count +1
            self.up[0:40]=self.up[1:41]
            self.up[40]=self.l
            self.pub.publish(self.vel)
            rospy.sleep (0.1)

if __name__ == '__main__':
    rospy.init_node('vel_publisher')
    datw = driving_along_the_wall()
    try:
        datw.run()
    except rospy.ROSInterruptException:
        pass
