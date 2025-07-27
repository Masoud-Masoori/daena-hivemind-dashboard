#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from pynput import keyboard
import sys

pressed_keys = set()

def update_motion(pub):
    twist = Twist()
    if 'w' in pressed_keys:
        twist.linear.x = 2.0
    elif 's' in pressed_keys:
        twist.linear.x = -2.0

    if 'a' in pressed_keys:
        twist.angular.z = 2.0
    elif 'd' in pressed_keys:
        twist.angular.z = -2.0

    pub.publish(twist)

def on_press(key):
    try:
        k = key.char.lower()
        if k in ['w', 'a', 's', 'd']:
            pressed_keys.add(k)
            update_motion(pub)
    except AttributeError:
        pass

def on_release(key):
    try:
        k = key.char.lower()
        if k in pressed_keys:
            pressed_keys.remove(k)
            update_motion(pub)
    except AttributeError:
        pass

    if key == keyboard.Key.esc:
        return False

if __name__ == '__main__':
    turtle_name = sys.argv[1] if len(sys.argv) > 1 else 'turtle1'
    rospy.init_node('keyboard_controller_' + turtle_name)
    pub = rospy.Publisher('/' + turtle_name + '/cmd_vel', Twist, queue_size=10)
    rospy.sleep(1)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
