# RobotProject
> cd <your_workspace>/src <br>
> git clone https://github.com/Kanyanat-Uetrakulchai/RobotProject.git <br>
> cd .. <br>
> rm -rf build install log <br>
> colcon build <br>
> export GZ_SIM_RESOURCE_PATH=$HOME/turtlebot3_ws/src/RobotProject/World/models:$GZ_SIM_RESOURCE_PATH <br>
> source install/setup.bash <br>
> export TURTLEBOT3_MODEL=burger <br>
> ros2 launch turtlebot3_gazebo empty_world.launch.py