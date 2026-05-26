#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np

class CollisionAvoidance(Node):

    def __init__(self):
        super().__init__('collision_avoidance')

        self.robot_id = self.declare_parameter('robot_id', 0).value

        self.pose = np.zeros(2)

        self.goal = np.array([5.0, 5.0])

        self.obstacles = [
            np.array([2.0, 2.0]),
            np.array([3.5, 1.5])
        ]

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

    def attractive_force(self):
        return self.goal - self.pose

    def repulsive_force(self):

        total = np.zeros(2)

        for obs in self.obstacles:

            diff = self.pose - obs
            dist = np.linalg.norm(diff)

            if dist < 1.5:
                total += 1.0 * (1.0/dist - 1.0/1.5) * (1.0/(dist**2)) * (diff/dist)

        return total

    def control_loop(self):

        u = self.attractive_force() + self.repulsive_force()

        cmd = Twist()
        cmd.linear.x = float(np.clip(u[0], -0.5, 0.5))
        cmd.angular.z = float(np.clip(u[1], -1.0, 1.0))

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
