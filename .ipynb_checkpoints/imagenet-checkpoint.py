import jetson.inference
import jetson.utils

import argparse
import sys


# parse the command line
parser = argparse.ArgumentParser(description="Classify a live camera stream using an image recognition DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.imageNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="")
parser.add_argument("--network", type=str, default="googlenet", help="")
parser.add_argument("--camera", type=str, default="0", help="")
parser.add_argument("--width", type=int, default=1280, help="")
parser.add_argument("--height", type=int, default=720, help="")
parser.add_argument('--headless', action='store_true', default=(), help="")

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)


# load the recognition network
net = jetson.inference.imageNet(opt.network, sys.argv)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)
font = jetson.utils.cudaFont()

# process frames until the user exits
while True:
	# capture the next image
	img = input.Capture()

	# classify the image
	class_id, confidence = net.Classify(img)

	# find the object description
	class_desc = net.GetClassDesc(class_id)

	# overlay the result on the image	
	#font.OverlayText(img, img.width, img.height, "{:05.2f}% {:s}".format(confidence * 100, class_desc), 5, 5, font.White, font.Gray40)
	
	# render the image
	#output.Render(img)

	# update the title bar
	#output.SetStatus("{:s} | Network {:.0f} FPS".format(net.GetNetworkName(), net.GetNetworkFPS()))

	#net.PrintProfilerTimes()
	# exit on input/output EOS
    
	if not input.IsStreaming() or not output.IsStreaming():
		break

	


