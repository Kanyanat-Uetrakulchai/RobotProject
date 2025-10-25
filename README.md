# RobotProject
> cd <your_workspace>/src <br>
> git clone https://github.com/Kanyanat-Uetrakulchai/RobotProject.git <br>
> export GZ_SIM_RESOURCE_PATH=`<PATH TO PROJECT>/RobotProject/World/models:$GZ_SIM_RESOURCE_PATH` <br>
> cd .. <br>
> rm -rf build install log <br>
> colcon build <br>
> source install/setup.bash <br>
> export TURTLEBOT3_MODEL=burger <br>
> ros2 launch turtlebot3_gazebo empty_world.launch.py world:=`<PATH TO PROJECT>/RobotProject/World/restaurant.sdf`

ถ้า Local Resources ใน Gazebo Sim ไม่ขึ้นแบบในภาพ
![alt text](image.png)
- ลอง `echo $GZ_SIM_RESOURCE_PATH` ถ้ามี `<PATH TO PROJECT>/RobotProject/World/models:$GZ_SIM_RESOURCE_PATH` ขึ้นแล้วแสดงว่าเพิ่มสำเร็จ
- รีสตาร์ทเครื่อง แล้วเปิดโปรแกรมใหม่ ถ้ายังไม่ขึ้นอีกให้รอไปสักพักแล้วค่อยรีสตาร์ทอีกรอบ โปรแกรมมันเปลี่ยนค่อนข้างช้า
