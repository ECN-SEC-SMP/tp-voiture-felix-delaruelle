# openCV import
import cv2 as cv
import sys
import time
import numpy as np


# Keycode definitions
ESC_KEY = 27
Q_KEY = 113

def getVideoProperties(cap):
    frameCount = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv.CAP_PROP_FPS))
    duration = frameCount/fps
    videoHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    videoWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))

    print("Nombre d'images total : " , frameCount)
    print("Nombre d'images par seconde : ", fps)
    print("Durée de la vidéo : ", duration)
    print("Résolution de la vidéo : " + str(videoWidth) + "x" + str(videoHeight))

    return frameCount, fps, duration, videoHeight, videoWidth

def main():
    # Define variables
    filename = sys.argv[1] if len(sys.argv) > 1 else '../video/video.avi'

    # Reading the image (and forcing it to grayscale)
    cap = cv.VideoCapture(filename)

    frameCount, fps, duration, videoHeight, videoWidth = getVideoProperties(cap)

    run = cap.isOpened()
   # Making sure the capture has opened successfully
    if not run:
        # capture opening has failed we cannot do anything :'(
        print("capture opening has failed we cannot do anything :'(")
        sys.exit()

    #Creating a window to display some images
    #cv.namedWindow("Original video")
    #cv.namedWindow("Gray video")
    cv.namedWindow('test numpy array display')
    
    # A key that we use to store the user keyboard input
    key = None
    # Waiting for the user to press ESCAPE before exiting the application
    imagesArray = np.empty((frameCount, videoHeight, videoWidth, 3), np.dtype('uint8'))
    fc = 0

    while key != ESC_KEY and key!= Q_KEY:
        ret, im = cap.read()
        if not ret:
            break
        imGray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)  
        #cv.imshow("Original video", im)
        #cv.imshow("Gray video", imGray)

        imagesArray[fc] = im
        cv.imshow('test numpy array display', imagesArray[fc])

        fc += 1

        # Look for pollKey documentation
        key = cv.pollKey()

    # release cap
    cap.release()
    # Destroying all OpenCV windows
    cv.destroyAllWindows()
    

if __name__ == "__main__":
    main()
