# openCV import
import cv2 as cv
import sys
import time


# Keycode definitions
ESC_KEY = 27
Q_KEY = 113

def getVideoProperties(cap):
    nbFrame = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv.CAP_PROP_FPS))
    duration = nbFrame/fps
    videoHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    videoWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))

    print("Nombre d'images total : " , nbFrame)
    print("Nombre d'images par seconde : ", fps)
    print("Durée de la vidéo : ", duration)
    print("Résolution de la vidéo : " + str(videoWidth) + "x" + str(videoHeight))

def main():
    # Define variables
    filename = sys.argv[1] if len(sys.argv) > 1 else '../video/video.avi'

    # Reading the image (and forcing it to grayscale)
    cap = cv.VideoCapture(filename)

    getVideoProperties(cap)

    run = cap.isOpened()
   # Making sure the capture has opened successfully
    if not run:
        # capture opening has failed we cannot do anything :'(
        print("capture opening has failed we cannot do anything :'(")
        sys.exit()

    #Creating a window to display some images
    cv.namedWindow("Original video")
    cv.namedWindow("Gray video")
    
    # A key that we use to store the user keyboard input
    key = None
    # Waiting for the user to press ESCAPE before exiting the application
    
    while key != ESC_KEY and key!= Q_KEY:
        ret, im = cap.read()
        imGray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)  
        cv.imshow("Original video", im)
        cv.imshow("Gray video", imGray)

        # Look for pollKey documentation
        key = cv.pollKey()
    
    
    # release cap
    cap.release()
    # Destroying all OpenCV windows
    cv.destroyAllWindows()
    

if __name__ == "__main__":
    main()
