#!/usr/bin/env python3
import rospy
import random
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
V_CONSTANT = 0.5
W_CONSTANT = 1.0
RATE_CONSTANT = 10
class FollowerTurtle:

    def __init__(self, name):
        # rospy.init_node(name, anonymous = True)
        self.turtle_x = random.random() * 10
        self.turtle_y = random.random() * 10
        self.turtle_theta = 0.0
        self.goal_x, self.goal_y = 0.0, 0.0
        self.name = name
        rospy.wait_for_service('/spawn')

        try:
    
            spawn_turtle = rospy.ServiceProxy('/spawn', Spawn)
            spawn_turtle(self.turtle_x, self.turtle_y, 0, name)
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed: {e}")
            

        rospy.Subscriber(f'/{self.name}/pose', Pose, self.pose_callback)

    def pose_callback(self,position_data):
        self.turtle_x = position_data.x
        self.turtle_y = position_data.y
        self.turtle_theta = position_data.theta
        # rospy.loginfo(f"Turtle Position: x={turtle_x}, y={turtle_y}, theta={turtle_theta}")

    def master_callback(self, master_data):
        self.goal_x = master_data.x
        self.goal_y = master_data.y

    def move_to_goal(self):
        pub = rospy.Publisher(f'/{self.name}/cmd_vel', Twist, queue_size = 10)
        rospy.Subscriber('/turtle1/pose', Pose, self.master_callback)
        rate = rospy.Rate(RATE_CONSTANT)
        vel_cmd = Twist()
        while not rospy.is_shutdown():
            distance = math.sqrt(math.pow((self.goal_x-self.turtle_x), 2) + math.pow((self.goal_y-self.turtle_y), 2))
            if (distance < 0.5):
                pub.publish(Twist())
                break
            goal_theta = math.atan2((self.goal_y - self.turtle_y),(self.goal_x - self.turtle_x))
            angular_diff = goal_theta - self.turtle_theta
            angular_diff = math.atan2(math.sin(angular_diff), math.cos(angular_diff))
            angular_velocity = W_CONSTANT * angular_diff
            vel_cmd.linear.x = V_CONSTANT
            vel_cmd.angular.z = angular_velocity  
            pub.publish(vel_cmd)
            rate.sleep()
        



    