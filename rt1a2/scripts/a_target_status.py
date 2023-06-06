"""
.. module:: a_target_status
   :platform: Unix
   :synopsis: Python module for the action client
.. moduleauthor:: Rafael Rabbani
This module provides a user interface for sending goals to an action server using the SimpleActionClient. The user can choose to send a target position goal to the server or cancel an ongoing goal.
"""
#! /usr/bin/env python3

import rospy
import actionlib
import actionlib.msg
import assignment_2_2022.msg
import os
import sys

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
# from msg import custom_odom


# callback function for the subscriber
# it pulls the data from the topic /odom and publishes it as a custom message
# the custom message is defined in the msg folder of the package rta1a2 (see the file custom_odom.msg)
# @param data: data from the topic /odom
# @type data: Odometry
# @return: none
def callback(data):
    """
	Callback function for the subscriber.
	It pulls the data from the topic /odom and publishes it as a custom message.
	Args:
		data (Odometry): Data from the topic /odom.
	Returns:
		None
	"""

    status_publish = rospy.Publisher('odom_custom', custom_odom, queue_size=5)  # create a publisher for the custom message named odom_custom
    status = custom_odom()    # create a custom message object
    status.x = data.pose.pose.position.x         # fill the custom massage x field with the x position from the topic /odom
    status.y = data.pose.pose.position.y         # fill the custom massage y field with the y position from the topic /odom
    status.vel_x = data.twist.twist.linear.x     # fill the custom massage vel_x field with the x velocity from the topic /odom
    status.vel_y = data.twist.twist.linear.y     # fill the custom massage vel_y field with the y velocity from the topic /odom
    status_publish.publish(status)   # publish the custom message named odom_custom

# set the target for the robot function (action client)
# it sends user inpud target (x,y) to the action server
# @param none
# @return: none
def set_target():
    """
    Set the target for the robot (action client).
    It sends user input target (x, y) to the action server.

    Args:
        None
    Returns:
        None
    """

    target_x = input("Enter target x: ")    # get the target x from the user
    target_y = input("Enter target y: ")    # get the target y from the user    
    target_x = int(target_x)    # convert the target x to int
    target_y = int(target_y)    # convert the target y to int

    print("\nWaiting for server...")        # print a message to the user that the client is waiting for the server
    client.wait_for_server()                # wait for the server to be up and running (the server is up and running when the action server node is running)
    print("Connected to the action server") # print a message to the user that the client is connected to the server
    
    goal = PoseStamped()    # create a PoseStamped object 
    goal.pose.position.x = target_x   # fill the goal x field with the target x
    goal.pose.position.y = target_y   # fill the goal y field with the target y
    #goal = assignment_2_2022.msg.PlanningGoal(goal)  # create a PlanningGoal object 
    print("\nSending goal to the server...")    # print a message to the user that the client is sending the goal to the server
    client.send_goal(goal)                      # send the goal to the server 
    print("Goal sent to the server")            # print a message to the user that the client sent the goal to the server
    #rospy.sleep(2)                              # wait for 2 seconds
    menu()                                      # call the menu function to show the menu again to the user 

# cancel the target for the robot function (action client)
# it sends a cancel request to the action server
# @param none
# @return: none
def cancel_target():
    """
    Cancel the target for the robot (action client).
    It sends a cancel request to the action server.

    Args:
        None
    Returns:
        None
    """
    print("\nCanceling goal...")   # print a message to the user that the client is canceling the goal
    client.cancel_goal()           # cancel the goal
    print("Goal canceled")         # print a message to the user that the client canceled the goal
    #rospy.sleep(2)                 # wait for 2 seconds
    menu()                         # call the menu function to show the menu again to the user

# error function
# it prints an error message if the user input is not acceptable
# @param none
# @return: none
def error():
    """
    Error function.
    It prints an error message if the user input is not acceptable.

    Args:
        None
    Returns:
        None
    """
    print("Input unacceptable")     # print an error message to the user
    #rospy.sleep(2)                  # wait for 2 seconds
    menu()                          # call the menu function to show the menu again to the user

# menu function 
# it prints the menu containing what the node does and the options for the user
# the user can choose to set a target or to cancel the target
# if 1 is entered, the set_target function is called
# if 2 is entered, the cancel_target function is called
# if any other input is entered, the error function is called
# @param none
# @return: none
def menu():
    os.system('clear')  # clear the terminal
    print("\n\n*************************************************************************")
    print(" A.\n     This node implements an action client, \n     allowing the user to set a target (x, y) or to cancel it.")
    print("     The node also publishes the robot position and velocity \n     as a custom message (x,y, vel_x, vel_z)")
    print("     by relying on the values published on the topic /odom.")
    print("*************************************************************************")
    print("Press 1 for Set Target")
    print("Press 2 for Cancel Target\n")  

    user_selection = input("What's in your mind : ") # get the user input
    if   (user_selection == "1"):
        set_target()
    elif (user_selection == "2"):
        cancel_target() 
    else:
        error()

# main function
# it initializes the node, creates a subscriber for the topic /odom and an action client for the action server named reaching_goal 
# it also calls the menu function to show the menu to the user 
if __name__ == '__main__':
    try:
        rospy.init_node('a_target_status')  # initialize the node named a_target_status
        rospy.Subscriber("/odom", Odometry, callback) # create a subscriber for the topic /odom and call the callback function when a message is received 
        client = actionlib.SimpleActionClient('/reaching_goal',assignment_2_2022.msg.PlanningAction )   # create an action client for the action server named reaching_goal 
        menu()  # call the menu function to show the menu to the user
        rospy.spin()   # keep the node running
    # if the node is interrupted, print an error message to the user
    except rospy.ROSInterruptException:
        #print("program interrupted before completion", file=sys.stderr)
        pass