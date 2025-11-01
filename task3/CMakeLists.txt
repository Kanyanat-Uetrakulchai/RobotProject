cmake_minimum_required(VERSION 3.8)
project(task3)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "action/ServeFood.action"
  DEPENDENCIES builtin_interfaces
)

set(AM_PYTHON_INSTALL_UNIQUE TRUE)
ament_python_install_package(${PROJECT_NAME}_pkg PACKAGE_DIR .)

install(PROGRAMS
  scripts/server_node.py
  scripts/client_node.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
