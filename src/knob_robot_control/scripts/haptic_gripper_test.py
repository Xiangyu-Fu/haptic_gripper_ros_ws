#!/usr/bin/env python
# 
import rospy
from knob_robot_control.msg import KnobState, KnobCommand
import math

class HapticGripperNode:
    def __init__(self):
        rospy.init_node('haptic_gripper_node', anonymous=True)
        rospy.on_shutdown(self.shutdown)

        # init some parameters
        self.force = None
        self.gripper_state = None
        self.last_force = 0.0

        # subscribe to the topic
        rospy.Subscriber("/knob_state", KnobState, self.knob_state_callback, queue_size=1 )

        # publish to the topic
        self.knob_command_pub = rospy.Publisher("/knob_command", KnobCommand, queue_size=10)


    def force_testing(self) -> None:
        # when state between 0-50, apply force 0.0
        # when state between 50-100, apply force from 0.0 to 2.0
        if self.gripper_state is not None :
            if self.gripper_state < 50:
                # self.publish_force(0.0)
                current_force = 0.0
            elif self.gripper_state < 100:
                # self.publish_force(2.0 * self.gripper_state / 100.0)
                current_force = 4.0 * self.gripper_state / 100.0
            else:
                # self.publish_force(2.0)
                current_force = 2.0
            self.publish_force(current_force)
            # if self.last_force != current_force:
            #     self.publish_force(current_force)
            #     self.last_force = current_force

    def publish_force(self, force=1.0) -> None:
        knob_command = KnobCommand()
        # (object position, object force) -> knob
        knob_command.text.data = "force"
        knob_command.position.data = self.gripper_state
        knob_command.tcp_force.data = float(force)
        print("Force: ", force)
        self.knob_command_pub.publish(knob_command)

    def knob_state_callback(self, msg: KnobState) -> None:
        # when value changed, print the value
        if self.gripper_state != msg.position.data:
            rospy.loginfo("Gripper state: %s", msg.position.data)
        self.gripper_state = msg.position.data
        

    def run(self):
        rate = rospy.Rate(10)  

        while not rospy.is_shutdown():
            # Add your code here
            self.force_testing()
            rate.sleep()

    def shutdown(self):
        # rospy.loginfo("Shutting down ROS node")
        pass 

if __name__ == '__main__':
    try:
        node = HapticGripperNode()
        node.run()
    except rospy.ROSInterruptException:
        pass