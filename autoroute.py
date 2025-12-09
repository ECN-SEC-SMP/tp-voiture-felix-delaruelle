# openCV import
import cv2 as cv
import sys
import numpy as np

# Keycode definitions
ESC_KEY = 27
Q_KEY = 113

# Print video information
def videoInfo(cap):
    print("N (number of frames) : " + str(cap.get(cv.CAP_PROP_FRAME_COUNT)))
    print("length : " + str(cap.get(cv.CAP_PROP_FRAME_COUNT) / cap.get(cv.CAP_PROP_FPS)))
    print("width : " + str(cap.get(cv.CAP_PROP_FRAME_WIDTH)))
    print("height : " + str(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))

def main():
    # Define variables
    filename = sys.argv[1] if len(sys.argv) > 1 else 'video.avi'

    # Reading the image (and forcing it to grayscale)
    cap = cv.VideoCapture(filename)
    videobuf = np.empty((int(cap.get(cv.CAP_PROP_FRAME_COUNT)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
    
    run = cap.isOpened()
   # Making sure the capture has opened successfully
    if not run:
        # capture opening has failed we cannot do anything :'(
        print("capture opening has failed we cannot do anything :'(")
        sys.exit()

    videoInfo(cap)
    #Creating a window to display some images
    cv.namedWindow("Original video")
    cv.namedWindow("Gray video")
    
    # A key that we use to store the user keyboard input
    key = None
    fc = 0
    ret = True  
    # Waiting for the user to press ESCAPE before exiting the application
    
    while key != ESC_KEY and key!= Q_KEY and fc < int(cap.get(cv.CAP_PROP_FRAME_COUNT)) and ret:
        # store the video in a numpy array
        ret, videobuf[fc] = cap.read()
        imGray = cv.cvtColor(videobuf[fc], cv.COLOR_RGB2GRAY)
        cv.imshow("Original video", videobuf[fc])
        cv.imshow("Gray video", imGray)
        # Look for pollKey documentation
        key = cv.pollKey()
        # Increment frame counter
        fc += 1
    
    # release cap
    cap.release()
    # Destroying all OpenCV windows
    cv.destroyAllWindows()
    

if __name__ == "__main__":
    main()
