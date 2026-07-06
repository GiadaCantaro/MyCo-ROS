cmake_minimum_required(VERSION 3.8)
project(myco_basic_api)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(moveit_core REQUIRED)
find_package(moveit_ros_planning REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(control_msgs REQUIRED)
find_package(controller_manager_msgs REQUIRED)
find_package(myco_robot_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(tf2_eigen REQUIRED)

# --- IL FIX SUPREMO PER JAZZY ---
# Diamo al compilatore i due percorsi nascosti di MoveIt e di OMPL 1.5
include_directories(
  include
  /opt/ros/jazzy/include/moveit_planners
  /usr/include/ompl-1.5
)
# ---------------------------------

add_library(${PROJECT_NAME}_lib SHARED
  "src/myco_basic_api.cpp"
  "src/myco_teleop_api.cpp"
  "src/myco_motion_api.cpp"
)

set(DEPENDENCIES
  "rclcpp"
  "rclcpp_action"
  "std_msgs"
  "std_srvs"
  "sensor_msgs"
  "moveit_core"
  "moveit_ros_planning"
  "moveit_ros_planning_interface"
  "control_msgs"
  "controller_manager_msgs"
  "myco_robot_msgs"
  "tf2"
  "tf2_ros"
  "tf2_eigen"
)

# Colleghiamo la libreria OMPL di sistema
link_libraries(ompl)

ament_target_dependencies(${PROJECT_NAME}_lib ${DEPENDENCIES})

set(EXECUTABLE_NAME "myco_basic_api_node")

add_executable(${EXECUTABLE_NAME} 
  src/myco_basic_api_node.cpp
  src/myco_basic_api.cpp
  src/myco_teleop_api.cpp
  src/myco_motion_api.cpp
)

target_link_libraries(${EXECUTABLE_NAME} ${PROJECT_NAME}_lib ompl)
ament_target_dependencies(${EXECUTABLE_NAME} ${DEPENDENCIES})

install(TARGETS ${EXECUTABLE_NAME} ${PROJECT_NAME}_lib
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY include/
  DESTINATION include
)

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/myco_gui.py
  # Se in futuro farai altre GUI, ti basterà aggiungere il percorso qui sotto, es:
  # scripts/altra_gui.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
