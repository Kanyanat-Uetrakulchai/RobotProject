# RobotProject
> cd <your_workspace>/src <br>
> git clone https://github.com/Kanyanat-Uetrakulchai/RobotProject.git <br>
> cd .. <br>
> colcon build <br>
> export GZ_SIM_RESOURCE_PATH=PATH_TO_PTOJECT/RobotProject/World/models:$GZ_SIM_RESOURCE_PATH <br>
> source install/setup.bash <br>
> export TURTLEBOT3_MODEL=burger <br>
> ros2 launch turtlebot3_gazebo empty_world.launch.py
