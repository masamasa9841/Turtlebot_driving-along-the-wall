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
        self.sub2 = rospy.Subscriber('sentor', Float64, self.sentor_msg,queue_size=1)
        self.sub3 = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.bumper)
        self.vel = Twist()
        self.speed = 0.3
        self.kp = -3.0
        self.kp2 = 1.0
        self.left = 0.0
        self.sentor = 0.0
        self._hit_bumper = False

    def left_msg(self, msg):
        self.left = msg.data
        #print self.left

    def sentor_msg(self, msg):
        self.sentor = msg.data
        #print self.sentor

    def bumper(self, bumper):
        self._hit_bumper = True

    def run(self):
        while not rospy.is_shutdown():
            e = 0.4 - self.left
            p = e * self.kp
            p2 = self.sentor * 1.0
            if p2 > 0:
                p2 = self.speed
            elif p2 == 0:
                p2 = 0.05
            if self._hit_bumper:
                self.vel.linear.x = -0.01
                self.vel.angular.z = -4.0
                self.pub.publish(self.vel)
                time.sleep(0.2)
                self._hit_bumper = False
            else:
                self.vel.linear.x = p2
                if 3 < p:
                    self.vel.angular.z = 3
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
