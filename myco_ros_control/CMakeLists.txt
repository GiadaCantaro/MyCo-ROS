cmake_minimum_required(VERSION 3.8)
project(myco_ros_control)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(controller_manager REQUIRED)
find_package(controller_manager_msgs REQUIRED)
find_package(myco_robot_msgs REQUIRED)
find_package(trajectory_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(tf2 REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(controller_interface REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# --- INIZIO FIX PER IL DRIVER COMAU ---
# Cerchiamo l'header nella cartella install (che abbiamo verificato esistere)
find_path(MYCO_DRIVER_INCLUDE_DIR
  NAMES myco_ethercat_driver/myco_ethercat_driver.h
  PATHS ENV AMENT_PREFIX_PATH
  PATH_SUFFIXES include
)

# Cerchiamo la libreria .so DIRETTAMENTE nella tua cartella build temporanea!
find_library(MYCO_DRIVER_LIB
  NAMES myco_ethercat_driver_lib
  PATHS /home/comau/IsaacSim-ros_workspaces/jazzy_ws/build/myco_ethercat_driver
)

if(NOT MYCO_DRIVER_INCLUDE_DIR OR NOT MYCO_DRIVER_LIB)
  message(FATAL_ERROR "Ancora niente! Header trovato: ${MYCO_DRIVER_INCLUDE_DIR} | Libreria trovata: ${MYCO_DRIVER_LIB}")
endif()
# --- FINE FIX ---

set(DEPENDENCIES
  rclcpp
  rclpy
  std_msgs
  std_srvs
  controller_manager
  controller_manager_msgs
  myco_robot_msgs
  trajectory_msgs
  sensor_msgs
  tf2
  hardware_interface
  controller_interface
  pluginlib
  rosidl_default_generators
)

add_library(myco_hardware_interface SHARED
  src/myco_hardware_interface.cpp
  src/myco_hardware_onlyposition_interface.cpp
)

target_include_directories(myco_hardware_interface
  PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${MYCO_DRIVER_INCLUDE_DIR}
)

target_link_libraries(myco_hardware_interface
  ${MYCO_DRIVER_LIB}
)

ament_target_dependencies(myco_hardware_interface ${DEPENDENCIES})

pluginlib_export_plugin_description_file(hardware_interface myco_hardware_interface.xml)

install(
  TARGETS myco_hardware_interface
  LIBRARY DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY include/
  DESTINATION include
)

install(
  DIRECTORY 
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
