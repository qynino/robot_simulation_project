from launch import LaunchDescription
from launch.substitutions import (
    Command,
    FindExecutable,
    PathJoinSubstitution,
)
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("my_robot_description"), "urdf", "my_cobot.urdf.xacro"]
            )
        ]
    )

    load_gazebo= ExecuteProcess(
        cmd=['gazebo', "-s","libgazebo_ros_factory.so"],
        output='screen')
    

    spawn_robot = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-entity', 'my_robot',
                                   '-topic', 'robot_description',
                                  ],
                        output='screen'
    )

    # Robot state publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description_content}]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        load_gazebo,
        spawn_robot
        ])
