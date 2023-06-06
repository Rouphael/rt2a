## rt1a2
Università di Genova/MSc in Robotics Engineering/Research Track 1/2nd Assignment

**********************
**********************
**********************
**********************
**********************
# [UNIGE Università di Genova](https://unige.it/it/) , [MSc in Robotics Engineering](https://courses.unige.it/10635) , [Research_Track_1](https://unige.it/en/off.f/2021/ins/51201.html?codcla=10635) , Second Assignment
### Professor. [Carmine Recchiuto](https://github.com/CarmineD8)
### Autheor : [Rafael Rabbani](https://github.com/Rouphael)

**********************
**********************
**********************

# 1. Introduction
 This package consist of three nodes working along with the package [assignment_2_2022](https://github.com/CarmineD8/assignment_2_2022) that provides an implementation of an action server that moves a robot in the environment by implementing the bug0 algorithm. The three nodes are:
 1. a_target_publisher : This node implements an action client, allowing the user to set a target (x, y) or to cancel it. The node also publishes the robot position and velocity as a custom message (x,y, vel_x, vel_z) by subscribing to the odometry topic (/odom).
 2. b_goal_status : This node is a service node that, when called, prints the number of goals that have been reached and and the number of goals that have been cancelled.
 3. c_robot_subscriber : This node subscribes to the custom message published by the a_target_publisher node and calculates the distance between the robot and the target and the average speed of the robot. the node also prints the distance and the average speed on the terminal.

**********************
**********************
**********************

# 2. Installation

## 2.1 Guide for starter's (Ubuntu22 os installed)
 If you are new to ROS, you can follow the instruction below to install ROS,Gazebo and other dipendencies and create a workspace and use this package.

 **If you have already done so, you can skip to the next section.**

## 2.1.1 Preliminarly install gazebo
```bash
    sudo apt-get install -y gazebo libgazebo-dev
```
## 2.1.2 Add the ros repository
```bash
    sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu focal main" > /etc/apt/sources.list.d/ros-latest.list'
```
```bash
    sudo apt install curl gnupg
```
```bash
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
```
```bash
    sudo apt update
```
## 2.1.3 Install all needed software
```bash
    sudo apt-get install python3-rosinstall-generator python3-vcstools build-essential python3-pip wget
```
```bash
    sudo pip3 install -U rosdep
```
```bash
    sudo pip3 install wstool
```
## 2.1.4 Initialize the ros workspace
```bash
    sudo rosdep init
```
```bash
    rosdep update
```
```bash
    mkdir ~/ros_catkin_ws
``` 
```bash
    cd ~/ros_catkin_ws
```
```bash
    rosinstall_generator desktop_full --rosdistro noetic --deps --tar > noetic-desktop_full.rosinstall
```
```bash
    mkdir ./src
```
```bash
    wstool init src noetic-desktop_full.rosinstall
```
## 2.1.5 Install hddtemp manually and fix the workspace
```bash
    wget http://archive.ubuntu.com/ubuntu/pool/universe/h/hddtemp/hddtemp_0.3-beta15-53_amd64.deb  
```
```bash
    sudo apt install ./hddtemp_0.3-beta15-53_amd64.deb
```
```bash
    rm hddtemp_0.3-beta15-53_amd64.deb
```
```bash
    cd src/diagnostics/diagnostic_common_diagnostics
```
Open the file package.xml and delete line 21
```bash
    gedit package.xml
```
In following folder
```bash
    cd ../../rosconsole/src/rosconsole/impl/
```
Replace rosconsole_log4cxx.cpp with 
https://raw.githubusercontent.com/AchmadFathoni/rosconsole/c9d161a6d946590bf808eb6006430c8c8d8b5cd6/src/rosconsole/impl/rosconsole_log4cxx.cpp

In following folder
```bash
    cd ../../../../roscpp_core/roscpp_serialization/include/ros/
```
Replace serialization.h with

https://raw.githubusercontent.com/ros/roscpp_core/noetic-devel/roscpp_serialization/include/ros/serialization.h

In following folder :
```bash
    cd ../../../../laser_geometry
```
Open CMAkeLists.txt and change line 4 with: set(CMAKE_CXX_STANDARD 17)

In following folder :
```bash
    cd ../laser_filters
```
Open CMAkeLists.txt and change line 4 with: set(CMAKE_CXX_STANDARD 17)

In following folder :
```bash
    cd ../urdf/urdf
```
Open CMAkeLists.txt and change line 25 with: set(CMAKE_CXX_STANDARD 20)

In following folder :
```bash
    cd ../../kdl_parser/kdl_parser
```
Open CMAkeLists.txt and change line 5 with: set(CMAKE_CXX_STANDARD 20)

In following folder :
```bash
    cd ../../rviz
```
Open CMAkeLists.txt and add line 3: set(CMAKE_CXX_STANDARD 17)

In following folder :
```bash
    cd ../rqt_rviz
```
Open CMAkeLists.txt and add line 4: set(CMAKE_CXX_STANDARD 17)

In following folder :
```bash
    cd ../visualization_tutorials/librviz_tutorial
```
Open CMAkeLists.txt and add line 15 with: set(CMAKE_CXX_STANDARD 17)

In following folder :
```bash
    cd ../rviz_plugin_tutorials
```
Open CMAkeLists.txt and add line 8: set(CMAKE_CXX_STANDARD 17)

In following folder :
```bash
    cd ../../perception_pcl/pcl_ros
```
Open CMAkeLists.txt and change line 9 with: set(CMAKE_CXX_STANDARD 17)

In following folder :
```bash
    cd ../../gazebo_ros_pkgs/gazebo_plugins
```
Open CMAkeLists.txt and add line 5: set(CMAKE_CXX_STANDARD 17)

In following folder :
```bash
    cd ../gazebo_ros_control
```
Open CMAkeLists.txt and add line 3: set(CMAKE_CXX_STANDARD 17)

In following folder :
```bash
    cd ../gazebo_ros
```
Open CMAkeLists.txt and add line 3: set(CMAKE_CXX_STANDARD 17)

```bash
    cd ../../..
```
## 2.1.6 Install all the dependencies
```bash
    rosdep install --from-paths ./src --ignore-packages-from-source --rosdistro noetic -y
```
## 2.1.7 Build the workspace
```bash
    ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_STANDARD=20
```
## 2.1.8 Setup the .basrhc script
```bash
    cd ..
```
Open .bashrc with a text editor and add the following line at the end of the file: 

source ~/ros_catkin_ws/install_isolated/setup.bash
```bash
    source .bashrc
```
You should have now a full desktop ROS installation in your Ubuntu22 OS!

**********************
# 2.2 Guide with ROS and dependencies installed
**Those who already have ROS and dependencies installed can skip the first part of the guide and start from here.**

## 2.2.1 Install the package
Go to the src folder of your workspace
```bash
    cd ~/ros_catkin_ws/src
```
Clone the repository [assignment_2_2022](https://github.com/CarmineD8/assignment_2_2022)
in the src folder
```bash
    git clone https://github.com/CarmineD8/assignment_2_2022.git
```
Clone the repository [rt1a2](https://github.com/Rouphael/rt1a2) in the src folder
```bash
    git clone git@github.com:Rouphael/rt1a2.git
```
Go to your workspace root folder
```bash
    cd ~/ros_catkin_ws/
```
Build any packages located in ~/catkin_ws/src.
```bash
    Catkin_make
```
**********************
**********************
**********************
# 3. Running the package
**You can easily run the package by launching the rt1a2.launch file.**

Open a terminal and type
```bash
    roslaunch rt1a2 rt1a2.launch
```
**This will do the following:**
* Launch assignment1.launch placed in the assignment_2_2022 package
  * Launch sim_w1.launch 
  * Set the parameters for the robot
  * Launch wall_follower
  * Launch go_to_point
  * Launch bug_action_service
* Launch a_target_status
* Launch b_goal_status
* Launch c_bug_action_client

Now you have Gazebo simuulation with a robot and walls, RViz with the robot model and the laser data, and three terminals oppened.

![gazebo](/pic/Gazebo.png)

![rviz](/pic/RViz.png)

**********************
**********************
**********************
# 4. Oppened terminals
## Terminal A. 
**In this terminal you can choose to set a target point or to cancel it.**
 If you want to set a target you can enter 1.

![t1](/pic/a_target_status%20start.png)

 Then you will be asked to enter the x and y coordinates of the target point.

![t2](/pic/a_taget_status%20target.png)


 If you want to cancel the target you can enter 2.

![t3](pic/a_target_status%20cancel.png)

## Terminal B.
**This terminal will show the number of goals reached and the number of goals cancelled when the service goal_status is called.**

![b1](pic/b_goal_status%20start.png)

For calling goal_status service open a terminal and type
```bash
    rosservice call /goal_status
```

![b2](pic/b_goal_status%20data.png)


## Terminal C.
**This terminal will show robot's distance from the target point and the average speed of the robot with an update rate of publish_speed in Hz.**

![c1](pic/c_robot_subscriber%20start.png)

Publish_speed is set to 2Hz by defult in rt1a2.launch file and you can change it by changing the value of publish_speed in rt1a2.launch file.
```bash
    <param name="publish_speed" value=" <custom update rate> "/>
```
or by oppening a terminal and typing
```bash
    rosparam set /publish_speed <custom update rate>
```

![c2](pic/c_robot_subscriber%20data.png)

**********************
**********************
**********************
# 5. Node description
## 5.1 a_target_status
**This node implements an action client, allowing the user to set a target (x, y) or to cancel it.**
**The node also publishes the robot position and velocity as a custom message (x,y, vel_x, vel_z) by relying on the values published on the topic /odom.**

This script is a python program that utilizes the ROS (Robot Operating System) framework to perform specific tasks. The script starts by importing necessary libraries and modules such as rospy, actionlib, and custom message types.

The script contains several functions that perform different tasks:

*    **callback(data)** - This function is a subscriber callback that listens to the '/odom' topic and pulls data from it. The data is then republished as a custom message, named 'odom_custom', using a publisher object. The custom message is defined in the 'msg' folder of the package 'rta1a2' (file: 'custom_odom.msg'). The function takes in one parameter 'data' which is of type Odometry, and it does not return anything.

*   **set_target()** - This function is an action client that sends user-inputted target (x,y) coordinates to an action server. The function prompts the user to enter the target x and y coordinates and converts them to integers. It then creates a PoseStamped object, fills the goal x and y fields with the target x and y, and creates a PlanningGoal object. The function then sends the goal to the server, prints a message to the user that the goal was sent, and waits for 2 seconds before calling the 'menu()' function again to display the menu options.

*    **cancel_target()** - This function is also an action client that sends a cancel request to the action server. It simply calls the 'client.cancel_goal()' function and prints a message to the user that the goal was canceled. It then waits for 2 seconds before calling the 'menu()' function again to display the menu options.

*    **error()** - This function is called when the user input is not acceptable. It simply prints an error message to the user, waits for 2 seconds, and calls the 'menu()' function again to display the menu options.

*    **menu()** - This function displays the menu options to the user, which are to set a target or to cancel the target. The user can enter '1' to call the 'set_target()' function, '2' to call the 'cancel_target()' function, or any other input to call the 'error()' function. The function also clears the terminal before displaying the menu options.
  
In summary, this script is a ROS node that listens to the '/odom' topic, republishes the data as a custom message, and allows the user to set or cancel a target using an action client. The script also has error handling and menu options to guide the user's interactions.

### Pseduo code for node a_target_status
    1. Define the callback function for the subscriber, which listens to the "/odom" topic
    2. In the callback function:
        a. Create a publisher for the custom message named "odom_custom"
        b. Create a custom message object
        c. Fill the custom message object's x, y, vel_x, and vel_y fields with the corresponding data from the "/odom" topic
        d. Publish the custom message "odom_custom"
    3. Define the set_target function:
        a. Get the target x and y coordinates from the user
        b. Convert the target x and y coordinates to int
        c. Print a message to the user that the client is waiting for the server
        d. Wait for the server to be up and running
        e. Print a message to the user that the client is connected to the server
        f. Create a PoseStamped object
        g. Fill the goal x and y fields with the target x and y coordinates
        h. Create a PlanningGoal object
        i. Print a message to the user that the client is sending the goal to the server
        j. Send the goal to the server
        k. Print a message to the user that the client sent the goal to the server
        l. Wait for 2 seconds
        m. Call the menu function to show the menu again to the user
    4. Define the cancel_target function:
        a. Print a message to the user that the client is canceling the goal
        b. Cancel the goal
        c. Print a message to the user that the client canceled the goal
        d. Wait for 2 seconds
        e. Call the menu function to show the menu again to the user
    5. Define the error function:
        a. Print an error message to the user
        b. Wait for 2 seconds
        c. Call the menu function to show the menu again to the user
    6. Define the menu function:
        a. Clear the terminal
        b. Print the menu containing what the node does and the options for the user
        c. Get the user's input
        d. If the user's input is 1, call the set_target function
        e. If the user's input is 2, call the cancel_target function
        f. If the user's input is any other value, call the error function
    7. Initialize the node
    8. Create a subscriber that listens to the "/odom" topic and calls the callback function when new data is received
    9. Create an action client and assign it to the variable "client"
    10. Call the menu function to show the menu to the user
    11. Keep the node running using a while loop, until the user exits the node manually.

## 5.2 b_goal_status
**This node is a service node that, when called , prints the number of goals reached and cancelled.**

This script is a ROS (Robot Operating System) node written in Python that serves as a service node. It listens to a topic called /reaching_goal/result and tracks the number of goals that have been reached and the number of goals that have been canceled. When the service is called, it prints the current number of goals reached and canceled to the console.

The script begins by importing the necessary modules, including rospy, a module specific to ROS that allows the node to interact with the ROS environment. It also imports a custom message called assignment_2_2022.msg, as well as the standard os and sys modules.

The script then defines several global variables: Number_goals_reached, Number_goals_canceled, and seq. The first two variables are used to keep track of the number of goals that have been reached and canceled, respectively. The seq variable is used to keep track of the number of times the service has been called.

* **service_callback(req)** - This callback function is defined for the service. This function is called whenever the service is called and it prints the current number of goals reached and canceled, as well as the current sequence number. It also returns an empty response.

* **subscriber_callback(data)** - This callback function is defined for the subscriber to /reaching_goal/. This function is called whenever a message is received on the /reaching_goal/result topic. It checks the status of the message, and if the status is 2 (canceled) it increments the Number_goals_canceled variable, and if the status is 3 (reached) it increments the Number_goals_reached variable.

* **menu(start)** - The function named menu is defined, which is used to print a menu to the console with information about the node's function. This function is called only once when the script is first run.

Finally, the script's __main__ function is executed. This function initializes the node, creates a subscriber and a service server, and then enters a loop to keep the node running. If the node is interrupted, the script will print an error message to the user.

The main function also calls the menu function for printing the menu only once, it initializes the node with name "b_goal_status" , it creates a subscriber to the topic "/reaching_goal/result" and it creates a service server named "goal_status". And it's doing a spin() to keep the node running.

### Pseduo code for node b_goal_status
    1. Define global variables Number_goals_reached, Number_goals_canceled, seq, and start.
    2. Define the service callback function
        a. Print the current seq number, number of goals reached, and number of goals canceled.
        b. ncrement the seq variable by 1.
        c. Return an empty response
    3. Define the subscriber callback function which listens to the "/reaching_goal/result" topic and check the status of the data object.
        a. If the status of the message is 2 (canceled), increment the Number_goals_canceled variable by 1
        b. If the status of the message is 3 (reached), increment the Number_goals_reached variable by 1
    4. Define the menu function
        a. Print the menu containing what the node does and the options for the user once
    5. Initialize the node with name "b_goal_status"
    6. Create a subscriber to the topic "/reaching_goal/result" and specify the subscriber_callback function as the callback.
    7. Create a service server named "goal_status" and specify the service_callback function as the callback.
    8. Use the rospy.spin() function to keep the node running, until the node is interrupted

## 5.3 c_robot_subscriber
**This node subscribes to the robot position and velocity (using the custom message odom_custom) and prints the distance of the robot from the target and the robot average speed. 
You can change publish_speed in rt1a2.launch to set how fast the node publishes the information.**

This script is a ROS (Robot Operating System) node written in Python that subscribes to the robot position and velocity (using the custom message) and prints the distance of the robot from the target and the robot average speed.

The script starts by importing the necessary libraries and modules: math, rospy, os, and sys.

Then it defines the following global variables:

*    average_speed: the average speed of the robot, initialized to 0
*    speed_data: a list of the last 10 robot speeds, initialized to 0 for all elements
*    goal_distance: the distance of the robot from the target, initialized to 6
*    start: a variable used to print the script's purpose only once, initialized to 1
  
The script then defines the following functions:

* **callback_subscriber(data)** -  callback function for the subscriber. It prints the distance of the robot from the target and the robot average speed. This function is called when a message is received. The function uses the pythagorean theorem to calculate the distance between the robot and the target using the robot's x and y position and the target's x and y position. It also calculates the robot's speed using the pythagorean theorem on the robot's x and y velocity. It then updates the list of the last 10 robot speeds and calculates the average speed of the robot.
* **menu(start)** -  prints the script's purpose, the distance of the robot from the target and the robot average speed. This function is called repeatedly in the main loop.

* **The if __name__ == "__main__"** -  block initializes the node, sets the rate at which the node publishes the information using the parameter /publish_speed from the launch file, initializes the subscriber to the topic odom_custom, and calls the menu() function in a loop until the node is shutdown.

In case of an interruption, the script will print an error message to the user.

### Pseduo code for node c_robot_subscriber
    1. Define global variables average_speed, speed_data, goal_distance, and start.
    2. Define the subscriber callback function
        a. Calculate the distance between the robot and the target using the robot's x and y position and the target's x and y position.
        b. Calculate the robot's speed using the pythagorean theorem on the robot's x and y velocity.
        c. Update the list of the last 10 robot speeds and calculate the average speed of the robot.
    3. Define the menu function
        a. Print the script's purpose, the distance of the robot from the target and the robot average speed.
    4. Initialize the node with name "c_robot_subscriber"
    5. Set the rate at which the node publishes the information using the parameter /publish_speed from the launch file
    6. Create a subscriber to the topic "odom_custom" and specify the callback_subscriber function as the callback.
    7. Call the menu function in  a loop until the node is shutdown.

**********************
**********************
**********************
Nodes Graph
![nodes](pic/rosgraph%20nodes.png)

Nodes and Topics Graph
![nodes](pic/rosgraph%20nodes%20and%20topics.png)

