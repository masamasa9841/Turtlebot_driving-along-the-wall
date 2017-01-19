#!/usr/bin/env python
import rospy
import time
from tf import TransformListener
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from sensor_msgs.msg import LaserScan
import math

class driving_along_the_wall(object):
    def __init__(self):
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.bumper)
        self.sub1 = rospy.Subscriber('/scan', LaserScan, self.laser)
        self.tf = TransformListener()
        time.sleep(2)
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
        self.count4 = 40
        self.count5 = 0
        self.count6 = 0
        self.count7 = 0
        self.count8 = 0
        self.heikin = 0
        self.kougo = 0
        self.front = 50
        self.first = 0
        self.stop = 0
        self.up=[]

    def tf_change(self):
            try:
                if self.tf.frameExists("/map") and self.tf.frameExists("/base_footprint"):
                    now = rospy.Time.now()
                    self.tf.waitForTransform("/map", "/base_footprint", now, rospy.Duration(2.0))
                    t = self.tf.getLatestCommonTime("/map", "/base_footprint")
                    position, quaternion = self.tf.lookupTransform("/map", "/base_footprint", t)
                else: position, quaternion = [0,0,0,0], [0,0,0,0]
            except:
                pass
            return position, quaternion

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
                self.heikin = 0
        self.heikin = self.heikin / self.count3
    def run (self):
        while not rospy.is_shutdown():
            p = 0
            while self.count <= 40:
                self.up.append(0.8)
                self.count = self.count +1
            if self.count8 > 0:
                print 1
                p = -0.8
                self.vel.linear.x = 0
                self.count8 += 1
                if self.count8 == 30:
                    self.count8 = 0
            elif self.ss <= 0.7 or self.count5 > 0:
                print 2
                p = -0.8
                self.vel.linear.x = -0.1
                self.count4 = 0
                self.front = 0
                self.count5 += 1
                if self.count5 == 8:
                    self.count5 = 0
                
            elif self.s == 1 or self.count6 > 0:
                print 3
                self.vel.linear.x = -0.1
                p = 0
                self.count6 += 1
                self.count7 = 0
                if self.count6 == 6:
                    self.count6 = 0
                    self.count8 = 1
            else:
                self.vel.linear.x = self.SPEED
                e = self.TARGET - self.heikin
                p = -e * 1.0
                self.count7 = 0
                print 'p'
                print p
                if math.fabs(p) >= 0.5:
                    e = self.TARGET - self.up[0]
                    p = -e*0.5
                    print 4
                    if math.fabs(p) >=1:
                        print 5
                        p = 0.3
                        self.vel.linear.x = 0.0
            self.vel.angular.z = p 
            if self.count4 == 0:
                while self.count4 < 30:
                    self.up[self.count4] = 0.8
                    self.count4 += 1
            while self.count <= 36:
                self.up.append(0.8)
                self.count = self.count +1
            self.up[0:35]=self.up[1:36]
            self.up[35]=self.heikin
            a, b = self.tf_change()
            if self.first == 50:
                x = a[0]
                y = a[1]
            if self.first > 200:
                if math.sqrt(math.pow(a[0]-x,2) + math.pow(a[1]-y,2)) < 1:
                    self.first = 51
                    self.stop += 1
                    print 7
            if self.stop == 3:
                print 6
                self.vel.linear.x = 0
                self.vel.angular.z = 0
            self.first += 1
            print 'a'
            print self.vel.linear.x 
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
