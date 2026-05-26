#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import numpy as np

class ConnectivityMonitor(Node):

    def __init__(self):
        super().__init__('connectivity_monitor')

        self.positions = {}

        for i in range(3):
            self.create_subscription(
                Odometry,
                f'/robot_{i}/odom',
                lambda msg, idx=i: self.callback(msg, idx),
                10
            )

        self.timer = self.create_timer(1.0, self.check_connectivity)

    def callback(self, msg, idx):
        self.positions[idx] = np.array([
            msg.pose.pose.position.x,
            msg.pose.pose.position.y
        ])

    def check_connectivity(self):

        ids = list(self.positions.keys())

        for i in range(len(ids)):
            for j in range(i+1, len(ids)):

                d = np.linalg.norm(
                    self.positions[ids[i]] - self.positions[ids[j]]
                )

                if d > 5.0:
                    self.get_logger().warn(
                        f'Connectivity risk between {ids[i]} and {ids[j]}'
                    )


def main(args=None):
    rclpy.init(args=args)
    node = ConnectivityMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
