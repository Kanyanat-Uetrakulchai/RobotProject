# RobotProject
> cd <your_workspace>/src <br>
> git clone https://github.com/Kanyanat-Uetrakulchai/RobotProject.git <br>
> sudo cp -r PATH_TO_PROJECT/RobotProject/World/models /opt/ros/jazzy/share/turtlebot3_gazebo/models/ <br>
> cd .. <br>
> rm -rf build install log <br>
> colcon build <br>
> source install/setup.bash <br>
> export TURTLEBOT3_MODEL=burger <br>
> ros2 launch turtlebot3_gazebo empty_world.launch.py world:=~/turtlebot3_ws/src/RobotProject/World/restaurant.sdf