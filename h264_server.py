#!/usr/bin/env python
import threading
import rospy
import socket
from roller_eye.msg import *

# TCP setup
TCP_IP = "0.0.0.0"  # Listen on all interfaces
TCP_PORT = 5005  # The port to listen on
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn = None

def accept_connections():
    global conn
    while not rospy.is_shutdown():
        try:
            conn, addr = s.accept()
            rospy.loginfo("Accepted new connection")
        except socket.error as e:
            rospy.logwarn("Socket error: %s", e)
        rospy.sleep(1)

def h264_callback(data):
    global conn
    if conn is not None:
        try:
            conn.send(bytearray(data.data))
        except socket.error as e:
            rospy.logwarn("Failed to send data: %s", e)
            conn = None

def main():
    rospy.init_node('h264_stream_listener', anonymous=True)
    rospy.Subscriber('/CoreNode/h264', frame, h264_callback)

    # Start a new thread to accept connections, so we don't block the main thread
    threading.Thread(target=accept_connections).start()

    rospy.spin()

if __name__ == '__main__':
    main()
