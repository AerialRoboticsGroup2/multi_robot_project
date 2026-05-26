#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class ConsensusNode(Node):

    def __init__(self):
        super().__init__('consensus_node')

        self.robot_id = self.declare_parameter('robot_id', 0).value

        self.value = random.uniform(0, 10)

        self.neighbor_values = {}

        self.pub = self.create_publisher(
            Float32,
            f'/robot_{self.robot_id}/consensus',
            10
        )

        for i in range(3):
            if i != self.robot_id:
                self.create_subscription(
                    Float32,
                    f'/robot_{i}/consensus',
                    lambda msg, idx=i: self.callback(msg, idx),
                    10
                )

        self.timer = self.create_timer(0.1, self.update)

    def callback(self, msg, idx):
        self.neighbor_values[idx] = msg.data

    def update(self):

        for val in self.neighbor_values.values():
            self.value += 0.1 * (val - self.value)

        msg = Float32()
        msg.data = float(self.value)

        self.pub.publish(msg)

        self.get_logger().info(f'Consensus value: {self.value}')


def main(args=None):
    rclpy.init(args=args)
    node = ConsensusNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
