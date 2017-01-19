#!/usr/bin/env python
import rospy
import time
from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import MapMetaData

class hoge(object):
    def __init__(self):
        rospy.init_node('mmap')
        self.sub = rospy.Subscriber('/map', OccupancyGrid, self.callback,queue_size=10)
        self.sub2 = rospy.Subscriber('/map_metadata', MapMetaData, self.callback2,queue_size=10)
        time.sleep(1)
        
    def callback(self, message):
        self.m = list(message.data)

    def callback2(self, message):
        self.w = message.width
        self.h = message.height

    def run(self):
        f = open('oppai.pgm', "w")
        f.write("P2\n")
        f.write("#masaya\n")
        f.write(str(self.w)+" "+str(self.h)+"\n")
        f.write("255\n")
        for i in range(1,int(self.h)):
            for j in range(0,int(self.w)):
                print int(self.w)*i-j
                #rospy.sleep(0.01)
                if self.m[int(self.w)*i-j] == 0:
                 self.m[int(self.w)*i-j] = "255"
                if self.m[int(self.w)*i-j] == -1:
                    self.m[int(self.w)*i-j] = "0"
                f.write(str(self.m[int(self.w)*i-j])+"\n")
        #while not rospy.is_shutdown():
        #    print self.m[1]
        #    rospy.sleep(1)
        f.close()

if __name__ == '__main__':
    t = hoge()
    t.run()

