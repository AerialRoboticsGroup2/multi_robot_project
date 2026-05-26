#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import numpy as np

class CoverageController(Node):

    def __init__(self):
        super().__init__('coverage_controller')

        self.robot_id = self.declare_parameter('robot_id', 0).value

        self.pose = np.zeros(2)

        self.centroid = np.array([0.0, 0.0])

        self.cmd_pub = self.create_publisher(
            Twist,
            f'/robot_{self.robot_id}/cmd_vel',
            10
        )

        self.create_subscription(
            Odometry,
            f'/robot_{self.robot_id}/odom',
            self.odom_callback,
            10
        )

        self.timer = self.create_timer(0.1, self.control_loop)

    def odom_callback(self, msg):
        self.pose[0] = msg.pose.pose.position.x
        self.pose[1] = msg.pose.pose.position.y

    def compute_centroid(self):

        # Placeholder Voronoi centroid
        return np.array([
            np.sin(self.get_clock().now().nanoseconds * 1e-9),
            np.cos(self.get_clock().now().nanoseconds * 1e-9)
        ])

    def control_loop(self):

        self.centroid = self.compute_centroid()

        error = self.centroid - self.pose

        cmd = Twist()
        cmd.linear.x = float(np.clip(error[0], -0.5, 0.5))
        cmd.angular.z = float(np.clip(error[1], -1.0, 1.0))

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = CoverageController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
