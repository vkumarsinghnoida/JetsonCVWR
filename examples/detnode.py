from jetson.inference import detectNet
from jetson.utils import videoSource, videoOutput
import sys
import serial
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ObjectDetection(Node):
    def __init__(self, network='ssd-mobilenet-v2', input='/dev/video0', output='/home/output.mp4', overlay='box,labels,conf', threshold=0.5):
        super().__init__('detector')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.net = detectNet(network, threshold=threshold)
        self.overlay = overlay
        self.video_source = videoSource(input)
        self.video_output = videoOutput(output)
        self.is_running = False
        self.arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

    def run(self):
        self.is_running = True
        msg = String()

        while self.is_running:
            img = self.video_source.Capture()
            detections = self.net.Detect(img, overlay=self.overlay)
            self.video_output.Render(img)
            print(detections)
            msg.data = str(detections)
            self.publisher_.publish(msg)
            if len(detections):
                self.arduino.write(bytes('12', 'utf-8'))
                time.sleep(0.05)
                data = self.arduino.readline()
                #print(data)
            else:
                self.arduino.write(bytes('1', 'utf-8'))
                time.sleep(0.05)
                data = self.arduino.readline()                
                print(data)
            if not self.video_source.IsStreaming() or not self.video_output.IsStreaming():
                break

def main(args):
    rclpy.init()
    obj_detection = ObjectDetection()
    obj_detection.run()
    obj_detection.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main(sys.argv)
