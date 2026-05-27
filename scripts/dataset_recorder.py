import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

import numpy as np

class DatasetRecorder(Node):

    def __init__(self):

        super().__init__('dataset_recorder')

        self.inputs = []
        self.outputs = []

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        self.current_scan = None

    def scan_callback(self, msg):

        ranges = np.array(msg.ranges)

        ranges[np.isinf(ranges)] = 10.0
        ranges[np.isnan(ranges)] = 10.0

        self.current_scan = ranges[:32]

    def cmd_callback(self, msg):

        if self.current_scan is None:
            return

        control = np.array([
            msg.linear.x,
            msg.angular.z
        ])

        self.inputs.append(self.current_scan)
        self.outputs.append(control)

    def save_dataset(self):

        X = np.array(self.inputs)
        Y = np.array(self.outputs)

        X = X.reshape((-1, 1, 32))

        np.save('training_inputs.npy', X)
        np.save('training_outputs.npy', Y)

        print('Dataset saved.')


def main(args=None):

    rclpy.init(args=args)

    node = DatasetRecorder()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.save_dataset()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
