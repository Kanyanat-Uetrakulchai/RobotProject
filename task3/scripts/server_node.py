#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient
from task3.action import ServeFood
from nav2_msgs.action import NavigateToPose
import math, asyncio
import time


class ServeFoodServer(Node):
    def __init__(self):
        super().__init__('serve_food_server')

        # สร้าง Action Server
        self._action_server = ActionServer(
            self,
            ServeFood,
            'serve_food',
            self.execute_callback
        )

        # เตรียม Nav2 client สำหรับ navigation
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # จุดพิกัดในแผนที่ (x, y, yaw)
        self.LOCATIONS = {
            "kitchen": (-0.041, 1.94, 0.0),
            "table_1": (0.688, -0.548, 0.0),
            "table_2": (-0.501, -0.7, 0.0),
            "table_3": (0.00241, -2.0, 0.0)
        }

    async def go_to_pose(self, x, y, yaw=0.0):
        """สั่งให้ Nav2 ไปยังพิกัด (x, y, yaw)"""
        self.get_logger().info("กำลังรอ Nav2 server...")
        ready = self.nav_client.wait_for_server(timeout_sec=15.0)
        if not ready:
            self.get_logger().error("Nav2 ยังไม่พร้อม!")
            return False

        # สร้าง goal message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.z = math.sin(yaw / 2.0)
        goal_msg.pose.pose.orientation.w = math.cos(yaw / 2.0)

        self.get_logger().info(f"ส่ง goal ไปยัง Nav2: ({x:.2f}, {y:.2f})")
        send_goal_future = self.nav_client.send_goal_async(goal_msg)
        goal_handle = await send_goal_future

        if not goal_handle.accepted:
            self.get_logger().warn("Nav2 ปฏิเสธ goal")
            return False

        self.get_logger().info("Nav2 ยอมรับ goal แล้ว กำลังเคลื่อนที่...")
        result_future = goal_handle.get_result_async()
        await result_future
        self.get_logger().info("ถึงจุดหมายเรียบร้อยแล้ว")
        return True

    async def execute_callback(self, goal_handle):
        """ภารกิจหลัก: ไปครัว -> โต๊ะที่สั่ง -> เสิร์ฟ"""
        feedback = ServeFood.Feedback()
        table_id = goal_handle.request.table_number
        table_key = f"table_{table_id}"

        # ตรวจว่ามีโต๊ะนี้จริงไหม
        if table_key not in self.LOCATIONS:
            feedback.status = f"ไม่พบโต๊ะ {table_id} ในระบบ!"
            goal_handle.publish_feedback(feedback)
            result = ServeFood.Result()
            result.success = False
            result.message = "โต๊ะไม่ถูกต้อง"
            goal_handle.abort()
            return result

        # --- เริ่มภารกิจ ---
        feedback.status = f"เริ่มภารกิจเสิร์ฟอาหารให้โต๊ะ {table_id}"
        self.get_logger().info(feedback.status)
        goal_handle.publish_feedback(feedback)
        time.sleep(2)

        # --- ไปครัว ---
        feedback.status = "กำลังไปครัวเพื่อรับอาหาร..."
        self.get_logger().info(feedback.status)
        goal_handle.publish_feedback(feedback)
        await self.go_to_pose(*self.LOCATIONS["kitchen"])

        feedback.status = "ถึงครัวแล้ว กำลังรับอาหาร..."
        self.get_logger().info(feedback.status)
        goal_handle.publish_feedback(feedback)
        time.sleep(5)  # จำลองการรอรับอาหาร5วินาที 

        # --- ไปโต๊ะ ---
        feedback.status = f"กำลังนำอาหารไปที่ {table_key}..."
        self.get_logger().info(feedback.status)
        goal_handle.publish_feedback(feedback)
        await self.go_to_pose(*self.LOCATIONS[table_key])

        # --- เสิร์ฟอาหาร ---
        feedback.status = f"ถึง {table_key} แล้ว กำลังเสิร์ฟอาหาร..."
        self.get_logger().info(feedback.status)
        goal_handle.publish_feedback(feedback)
        time.sleep(2)

        # --- จบภารกิจ ---
        result = ServeFood.Result()
        result.success = True
        result.message = f"เสิร์ฟอาหารที่ {table_key} ภารกิจเสร็จสิ้น!"
        goal_handle.succeed()
        self.get_logger().info(result.message)
        return result


def main(args=None):
    import asyncio
    rclpy.init(args=args)
    node = ServeFoodServer()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    node.get_logger().info("ServeFoodServer พร้อมรับคำสั่งแล้ว")
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
