import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

import numpy as np

import torch
import torch.nn as nn

# ======================================
# CNN MODEL
# ======================================

class CNNController(nn.Module):

    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv1d(1, 16, kernel_size=5)
        self.conv2 = nn.Conv1d(16, 32, kernel_size=5)

        self.relu = nn.ReLU()

        self.fc1 = nn.Linear(32 * 24, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 2)

    def forward(self, x):

        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))

        x = x.view(x.size(0), -1)

        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))

        return self.fc3(x)

# ======================================
# ROS2 NODE
# ======================================

class CNNControllerNode(Node):

    def __init__(self):

        super().__init__('cnn_controller')

        self.model = CNNController()

        self.model.load_state_dict(
            torch.load('models/cnn_controller.pth')
        )

        self.model.eval()

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

    def scan_callback(self, msg):

        ranges = np.array(msg.ranges)

        ranges[np.isinf(ranges)] = 10.0
        ranges[np.isnan(ranges)] = 10.0

        data = ranges[:32]

        data = data.reshape((1,1,32))

        tensor = torch.tensor(data, dtype=torch.float32)

        with torch.no_grad():
            output = self.model(tensor)

        linear = float(output[0][0])
        angular = float(output[0][1])

        cmd = Twist()

        cmd.linear.x = linear
        cmd.angular.z = angular

        self.cmd_pub.publish(cmd)

# ======================================
# MAIN
# ======================================


def main(args=None):

    rclpy.init(args=args)

    node = CNNControllerNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
