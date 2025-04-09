#!/usr/bin/env python3
import rospy
import threading
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
from follower_turtle import FollowerTurtle
STARTING_X = 5.544445
STARTING_Y = 5.544445
STARTING_THETA = 0.0
V_CONSTANT = 0.5
W_CONSTANT = 1.0
RATE_CONSTANT = 10
turtle_x, turtle_y, turtle_theta = STARTING_X, STARTING_Y, STARTING_THETA

def pose_callback(position_data):
    global turtle_x, turtle_y, turtle_theta
    turtle_x = position_data.x
    turtle_y = position_data.y
    turtle_theta = position_data.theta
    
    # rospy.loginfo(f"Turtle Position: x={turtle_x}, y={turtle_y}, theta={turtle_theta}")
def move_to_goal(goal_x, goal_y):
    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
    rate = rospy.Rate(RATE_CONSTANT)
    vel_cmd = Twist()
    while not rospy.is_shutdown():
        distance = math.sqrt(math.pow((goal_x-turtle_x), 2) + math.pow((goal_y-turtle_y), 2))
        if (distance < 0.1):
            print("stop")
            pub.publish(Twist())
            break
        goal_theta = math.atan2((goal_y - turtle_y),(goal_x - turtle_x))
        angular_diff = goal_theta - turtle_theta
        angular_diff = math.atan2(math.sin(angular_diff), math.cos(angular_diff))
        angular_velocity = W_CONSTANT * angular_diff
        vel_cmd.linear.x = V_CONSTANT
        vel_cmd.angular.z = angular_velocity  
        pub.publish(vel_cmd)
        rate.sleep()
      
def run_follower(turtle: FollowerTurtle):
    turtle.move_to_goal()

        
    
if __name__ == '__main__':
    rospy.init_node('multi_follower', anonymous=True)
    t1 = FollowerTurtle('greenturt')
    t2 = FollowerTurtle('redturt')
    thread_master = threading.Thread(target=move_to_goal, args=(3.4,4.5))
    thread2 = threading.Thread(target=run_follower, args=(t1,))
    thread3 = threading.Thread(target=run_follower, args=(t2,))
    thread_master.start()
    thread2.start()
    thread3.start()
    