#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from task3.action import ServeFood
import asyncio


class ServeFoodClient(Node):
    def __init__(self):
        super().__init__('serve_food_client')
        # ต้องชื่อเดียวกับฝั่ง Server
        self._action_client = ActionClient(self, ServeFood, 'serve_food')

    async def send_goal(self, table_number: int):
        """ส่งคำสั่งเสิร์ฟอาหารไปยังโต๊ะที่กำหนด"""
        self.get_logger().info("กำลังรอ Action Server ...")

        # รอ server แบบไม่ block event loop
        server_ready = await asyncio.to_thread(
            self._action_client.wait_for_server, timeout_sec=10.0
        )
        if not server_ready:
            self.get_logger().error("Server ยังไม่พร้อม!")
            return

        # ส่งหมายเลขโต๊ะจริง (1–3)
        goal_msg = ServeFood.Goal()
        goal_msg.table_number = table_number

        self.get_logger().info(f"ส่งออเดอร์เสิร์ฟอาหารไปยังโต๊ะ {table_number} ...")

        # ส่ง goal และรับ feedback callback
        send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback
        )
        goal_handle = await send_goal_future

        if not goal_handle.accepted:
            self.get_logger().warn("Server ปฏิเสธคำสั่ง")
            return

        self.get_logger().info("Server ยอมรับคำสั่งแล้ว กำลังดำเนินการ...")

        # รอผลลัพธ์สุดท้าย
        result_future = goal_handle.get_result_async()
        result = await result_future

        if result.result.success:
            self.get_logger().info(f"{result.result.message}")
        else:
            self.get_logger().info(f"{result.result.message}")

    def feedback_callback(self, feedback_msg):
        """แสดงข้อความ feedback ที่ได้รับจาก Server"""
        feedback = feedback_msg.feedback
        self.get_logger().info(f"[Feedback] {feedback.status}")


def main(args=None):
    import asyncio

    async def async_main():
        rclpy.init(args=args)
        node = ServeFoodClient()

        try:
            table_number = int(input("ป้อนหมายเลขโต๊ะที่ต้องการเสิร์ฟ (1,2,3): "))
            if table_number not in [1, 2, 3]:
                print("กรุณาเลือกเฉพาะโต๊ะ 1, 2 หรือ 3 เท่านั้น")
                node.destroy_node()
                rclpy.shutdown()
                return
        except ValueError:
            print("ต้องกรอกเป็นตัวเลขเท่านั้น")
            node.destroy_node()
            rclpy.shutdown()
            return

        # สั่ง goal แล้ว spin node แบบ await
        send_task = asyncio.create_task(node.send_goal(table_number))

        # ให้ ROS2 ทำงานใน thread แยก เพื่อไม่ block asyncio
        executor = rclpy.executors.MultiThreadedExecutor()
        spin_task = asyncio.to_thread(rclpy.spin, node, executor)

        # รอทั้งสองอย่าง (ส่ง goal + spin node) ไปพร้อมกัน
        await asyncio.gather(send_task, spin_task)

        node.destroy_node()
        rclpy.shutdown()

    asyncio.run(async_main())

if __name__ == '__main__':
    main()
