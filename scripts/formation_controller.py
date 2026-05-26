#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np

class FormationController(Node):

    def __init__(self):
        super().__init__('formation_controller')

        self.robot_id = self.declare_parameter('robot_id', 0).value

        self.cmd_pub = self.create_publisher(
            Twist,
            f'/robot_{self.robot_id}/cmd_vel',
            10
        )

        self.pose = np.zeros(2)
        self.neighbor_pose = np.zeros(2)

        self.create_subscription(
            Odometry,
            f'/robot_{self.robot_id}/odom',
            self.odom_callback,
            10
        )

        neighbor_id = (self.robot_id + 1) % 3

        self.create_subscription(
            Odometry,
            f'/robot_{neighbor_id}/odom',
            self.neighbor_callback,
            10
        )

        self.timer = self.create_timer(0.1, self.control_loop)

        self.desired_offset = np.array([1.0, 0.0])

    def odom_callback(self, msg):
        self.pose[0] = msg.pose.pose.position.x
        self.pose[1] = msg.pose.pose.position.y

    def neighbor_callback(self, msg):
        self.neighbor_pose[0] = msg.pose.pose.position.x
        self.neighbor_pose[1] = msg.pose.pose.position.y

    def control_loop(self):

        error = (self.pose - self.neighbor_pose) - self.desired_offset

        u = -1.0 * error

        cmd = Twist()
        cmd.linear.x = float(np.clip(u[0], -0.5, 0.5))
        cmd.angular.z = float(np.clip(u[1], -1.0, 1.0))

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = FormationController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
