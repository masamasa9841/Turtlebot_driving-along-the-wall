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
        self.SPEED = 0.1
        self.b = 3
        self.s = 0
        self.l = 0
        self.ss = 2
        self.count = 0
        self.count2 = 0
        self.count4 = 40
        self.count5 = 0
        self.count6 = 0
        self.heikin = 0
        self.kougo = 0
        self.front = 50
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
        self.m = len(laser.ranges) - 1
        self.heikin = 0
        self.count3 =0
        while self.m > len(laser.ranges)-30:
            if math.isnan(laser.ranges[self.m]) == False:
                self.heikin = laser.ranges[self.m] + self.heikin
                self.count3 += 1
            self.m -= 1
            if self.count3 == 0:
                self.count3 = 1
        self.heikin = self.heikin / self.count3

    def run (self):
        while not rospy.is_shutdown():
            p = 0
            if self.ss <= 0.7 or self.count5 > 0:
                p = -0.8
                self.vel.linear.x = 0
                self.count4 = 0
                self.front = 0
                self.count5 += 1
                print 'to1'
                if self.count5 == 8:
                    self.count5 = 0
                
            elif self.s == 1 or self.count6 > 0:
                self.vel.linear.x = 0
                p = -0.8
                self.count6 += 1
                print 'to2'
                if self.count6 == 10:
                    self.count6 = 0

            else:
                print 'to4'
                self.vel.linear.x = self.SPEED
                e = self.TARGET - self.heikin
                p = -e * 1.0
                if math.fabs(p) >= 2:
                    e = self.TARGET - self.up[0]
                    p = -e
                    print 1
                    if math.fabs(p) >= 4:
                        p = 4
                        print 22
            self.vel.angular.z = p *0.8
            if self.count4 == 0:
                while self.count4 < 71:
                    self.up[self.count4] = 0.8
                    self.count4 += 1
            while self.count <= 71:
                self.up.append(0.8)
                self.count = self.count +1
            self.up[0:70]=self.up[1:71]
            self.up[70]=self.heikin
            print 'ang'
            print self.vel.angular.z
            self.pub.publish(self.vel)
            rospy.sleep (0.1)

if __name__ == '__main__':
    rospy.init_node('vel_publisher')
    datw = driving_along_the_wall()
    try:
        datw.run()
    except rospy.ROSInterruptException:
        pass
