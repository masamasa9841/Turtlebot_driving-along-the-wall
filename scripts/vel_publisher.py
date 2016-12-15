#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from kobuki_msgs.msg import BumperEvent

class driving_along_the_wall(object):
    def __init__(self):
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
        self.sub = rospy.Subscriber('left', Float64, self.left_msg,queue_size=1)
        self.sub2 = rospy.Subscriber('center', Float64, self.center_msg,queue_size=1)
        self.sub3 = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.bumper)
        self.vel = Twist()
        self.speed = 0.7
        self.kp = -1.5
        self.kp2 = 1.0
        self.left   = [0.0,0.0,0.0,0.0,0.0]
        self.center = [0.0,0.0,0.0,0.0,0.0]
        self.ave = 0.0
        self.ave2 = 0.0
        self.hit_bumper = False

    def left_msg(self, msg):
        self.left.append(msg.data)
        self.left.pop(0)
        self.ave = sum(self.left) / len(self.left)

    def center_msg(self, msg):
        self.center.append(msg.data)
        self.center.pop(0)
        self.ave2 = sum(self.center) / len(self.center)
        print self.ave2

    def bumper(self, bumper):
        self.hit_bumper = True

    def run(self):
        while not rospy.is_shutdown():
            e = 0.4 - self.ave
            p = e * self.kp

            if self.ave2 > 0.4:
                p2 = self.speed
            else: 
                p2 = 0.05

            if self.hit_bumper:
                self.vel.linear.x = -0.05
                self.vel.angular.z = -1.0
                self.pub.publish(self.vel)
                time.sleep(0.2)
                self.hit_bumper = False

            else:
                self.vel.linear.x = p2

                if 5 < p:
                    self.vel.angular.z = 5.0

                elif -0.5 > p:
                    self.vel.angular.z = -0.5

                else:
                    self.vel.angular.z = p
                self.pub.publish(self.vel)
                rospy.sleep(0.01)


if __name__ == '__main__':
    rospy.init_node('vel_publisher')
    datw = driving_along_the_wall()
    try:
        datw.run()
    except rospy.ROSInterruptException:
        pass
