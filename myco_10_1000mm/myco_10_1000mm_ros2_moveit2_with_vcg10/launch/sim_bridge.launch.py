import os
from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_name = "myco_10_1000mm_ros2_moveit2_with_vcg10"
    
    moveit_config = (
        MoveItConfigsBuilder("MyCo-10-1_00", package_name=package_name)
        .robot_description(file_path="config/MyCo-10-1.00.urdf.xacro")
        .sensors_3d("config/sensors_3d.yaml")
        .to_moveit_configs()
    )
    rviz_config_file = os.path.join(get_package_share_directory(package_name), "config", "moveit.rviz")
    ros2_controllers_path = os.path.join(get_package_share_directory(package_name), "config", "ros2_controllers.yaml")
        
    ld = LaunchDescription()
    
    ld.add_action(SetParameter(name='use_sim_time', value=True))
    
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[moveit_config.robot_description, {'use_sim_time': True}]
    )
    
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[ros2_controllers_path, moveit_config.robot_description, {'use_sim_time': True}],
        remappings=[
            ("/controller_manager/robot_description", "/robot_description"),
        ],
        output="screen",
    )
    
    """
    move_group_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[moveit_config.to_dict(), {'use_sim_time': True}, {'octomap_resolution': 0.02}]
    )
    """
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        arguments=['-d', rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            {'use_sim_time': True}
        ]
    )

    spawner_jsb = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        parameters=[{'use_sim_time': True}]
    )

    spawner_arm = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['myco_arm_controller', '--controller-manager', '/controller_manager'], # <-- DEVE ESSERE IDENTICO ALLO YAML!
        parameters=[{'use_sim_time': True}]
    )

    ld.add_action(rsp_node)
    ld.add_action(ros2_control_node)  
    #ld.add_action(move_group_node)
    ld.add_action(rviz_node)
    ld.add_action(spawner_jsb)
    ld.add_action(spawner_arm)
    
    return ld
