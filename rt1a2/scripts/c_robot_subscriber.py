"""
.. module:: c_subscriber
   :platform: Unix
   :synopsis: Python module for the goal status
.. moduleauthor:: Ali Rabbani Doost

This script implements a service node that, when called, prints the number of goals reached and canceled. It also includes a subscriber to monitor goal status.
"""

#!/usr/bin/env python3

import math
import rospy
import os
import sys

#from rt1a2.msg import custom_odom

average_speed = 0
speed_data = [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]

goal_distance = 6
start = 1


# callback function for subscriber
# prints the distance of the robot from the target and the robot average speed
# this function is called when a message is received
# @param data: the message received
# @type data: rt1a2.msg.custom_odom
# @return: None
def callback_subscriber(data):
    """
    Callback function for the subscriber that prints the distance of the robot from the target and the robot's average speed.

    Args:
        data: The message received.

    Returns:
        None.

    This function is called when a message is received. It calculates the distance of the robot from the target using the Pythagorean theorem and updates the global variable 'goal_distance'. It also calculates the robot's speed using the Pythagorean theorem and updates the 'speed_data' list. The average speed is then calculated by summing all the elements in the list and dividing by 10. Finally, it calls the 'menu' function to print the distance and average speed.
    """
    global speed_data       # list of the last 10 robot speeds
    global average_speed    # average speed of the robot
    global goal_distance    # distance of the robot from the target

    des_pos_x = rospy.get_param("/des_pos_x")   # target x position
    des_pos_y = rospy.get_param("/des_pos_y")   # target y position
    status_x = data.x                           # robot x position
    status_y = data.y                           # robot y position
    goal_distance= math.sqrt(((des_pos_x - status_x)**2)+((des_pos_y - status_y)**2)) # calculate distance of the robot from the target using the pythagorean theorem

    status_vel_x = data.vel_x   # robot x velocity
    status_vel_y = data.vel_y   # robot y velocity
    robot_vel= math.sqrt((status_vel_x**2)+(status_vel_y**2)) # calculate robot speed using the pythagorean theorem 

    # update the list of the last 10 robot speeds
    # the list is updated by removing the first element and adding the new speed at the end
    # the average speed is calculated by summing all the elements in the list and dividing by 10
    for i in range(9):  
        speed_data[i] = speed_data[i+1] # remove first element from the list and shift all the elements to the left
    speed_data[9] = robot_vel           # add new speed to the list
    average_speed = sum(speed_data)/10  # calculate average speed of the robot

# menu function 
# it prints the menu containing what the node does
# it prints the distance of the robot from the target and the robot average speed
#@param start: a variable that is used to print what the node does only once
#@type start: int
#@return: None
def menu(start):
    """
    Menu function that prints the menu containing what the node does, the distance of the robot from the target, and the robot's average speed.

    Args:
        start: A variable that is used to print what the node does only once.

    Returns:
        None.
    """
    if start == 1:
        os.system('clear')
        print("\n*************************************************************************")
        print(" C.\n     This node subscribes to the robot position and velocity (using the custom message)")
        print("     and prints the distance of the robot from the target and the robot average speed.")
        print("     Change publish_speed in rt1a2.launch to set how fast the node publishes the information.")
        print("*************************************************************************\n") 
        start = 0
    print(f"Distance: {goal_distance}")
    print(f'Average Speed: {average_speed}')
    print("\n*************************************************************************\n") 

# main function
# it initializes the node and the subscriber and calls the menu function
if __name__ == "__main__":
    try:
        rospy.init_node('c_robot_subscriber')   # initialize the node
        rate = rospy.Rate(rospy.get_param("/publish_speed"))    # set the rate at which the node publishes the information (in Hz) from the launch file parameter publish_speed
        rospy.Subscriber("odom_custom", custom_odom, callback_subscriber) # initialize the subscriber to the topic odom_custom
        while not rospy.is_shutdown(): # loop until the node is shutdown
            menu(start)     # call the menu function
            rate.sleep() 
     # if the node is interrupted, print an error message to the user
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)
