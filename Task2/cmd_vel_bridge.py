#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped

class CmdVelBridge(Node):
    def __init__(self):
        super().__init__('cmd_vel_bridge')
        self.sub = self.create_subscription(Twist, '/cmd_vel_nav', self.listener_callback, 10)
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.get_logger().info('CmdVel Bridge started: /cmd_vel_nav → /cmd_vel')

    def listener_callback(self, msg: Twist):
        stamped = TwistStamped()
        stamped.twist = msg
        self.pub.publish(stamped)

def main():
    rclpy.init()
    node = CmdVelBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
