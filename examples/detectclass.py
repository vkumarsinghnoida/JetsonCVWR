from jetson.inference import detectNet
from jetson.utils import videoSource, videoOutput
import sys
import serial
import time

class ObjectDetection:
    def __init__(self, network='ssd-mobilenet-v2', input='/dev/video0', output='output.mp4', overlay='box,labels,conf', threshold=0.5):
        self.net = detectNet(network, threshold=threshold)
        self.overlay = overlay
        self.video_source = videoSource(input)
        self.video_output = videoOutput(output)
        self.is_running = False
        self.arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

    def run(self):
        self.is_running = True

        while self.is_running:
            img = self.video_source.Capture()
            detections = self.net.Detect(img, overlay=self.overlay)
            self.video_output.Render(img)
            print(detections)
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
    obj_detection = ObjectDetection()
    obj_detection.run()

if __name__ == '__main__':
    main(sys.argv)
