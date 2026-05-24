from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    nodes = []

    for i in range(3):

        nodes.append(
            Node(
                package='multi_robot_project',
                executable='formation_controller.py',
                parameters=[{'robot_id': i}]
            )
          )

        nodes.append(
            Node(
                package='multi_robot_project',
                executable='collision_avoidance.py',
                parameters=[{'robot_id': i}]
            )
        )

        nodes.append(
            Node(
                package='multi_robot_project',
                executable='coverage_controller.py',
                parameters=[{'robot_id': i}]
            )
        )
        nodes.append(
            Node(
                package='multi_robot_project',
                executable='consensus_node.py',
                parameters=[{'robot_id': i}]
            )
        )

    return LaunchDescription(nodes)
