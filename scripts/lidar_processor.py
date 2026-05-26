#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np

class LidarProcessor(Node):

    def __init__(self):
        super().__init__('lidar_processor')

        self.min_distance = 100.0

        self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

    def scan_callback(self, msg):

        ranges = np.array(msg.ranges)

        valid = ranges[np.isfinite(ranges)]

        if len(valid) > 0:
            self.min_distance = np.min(valid)
            self.get_logger().info(f'Min obstacle distance: {self.min_distance}')


def main(args=None):
    rclpy.init(args=args)
    node = LidarProcessor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
