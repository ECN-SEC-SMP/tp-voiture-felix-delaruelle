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

def calculateAverageImages(M, imagesArrayGray, imWidth, imHeight):
    meanImage = np.empty((imHeight, imWidth), np.dtype('uint8'))
    
    for i in range(imHeight):
        for j in range(imWidth):
            mean = 0
            for k in range(M):
                pixGrayLevel = imagesArrayGray[k][i][j]  # renvoie la valeur du niveau de gris du pixel
                mean += pixGrayLevel

            mean = mean / M
            meanImage[i][j] = int(mean)

    return meanImage

def detectRoad(meanImage, imageSequence, threshold, imWidth, imHeight, imCount):
    mask = np.empty((imHeight, imWidth), np.dtype('uint8'))
    res = np.empty((imCount, imHeight, imWidth), np.dtype('uint8'))
    
    for i in range(imHeight):
        for j in range(imWidth):
            meanDifference = 0
            for k in range(imCount):
                pixMeanImg = meanImage[i][j]
                pixImage = imageSequence[k][i][j]
                meanDifference += abs(int(pixImage) - int(pixMeanImg))
            
            meanDifference = meanDifference / imCount
            if meanDifference < threshold:
                mask[i][j] = 0
            else:
                mask[i][j] = 255

    for k in range(imCount):
        res[k] = cv.bitwise_and(imageSequence[k], imageSequence[k], mask=mask)

    return res

def detectCars(meanImage, imageSequence, threshold, imWidth, imHeight, imCount):
    res = np.empty((imCount, imHeight, imWidth), np.dtype('uint8'))
    
    for k in range(imCount):
        for i in range(imHeight):
            for j in range(imWidth):
                pixMeanImg = meanImage[i][j]
                pixImage = imageSequence[k][i][j]
                difference = abs(int(pixImage) - int(pixMeanImg))
                
                # Les voitures ont une grande différence avec la moyenne
                if difference > threshold:
                    res[k][i][j] = imageSequence[k][i][j]  # Garder le pixel original
                else:
                    res[k][i][j] = 0  # Mettre en noir (décor statique)

    return res

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
    cv.namedWindow('Mean image')
    cv.namedWindow('res')
    
    # A key that we use to store the user keyboard input
    key = None
    # Waiting for the user to press ESCAPE before exiting the application
    imagesArrayGray = np.empty((frameCount, videoHeight, videoWidth), np.dtype('uint8'))
    fc = 0

    while key != ESC_KEY and key!= Q_KEY:
        ret, im = cap.read()
        if not ret:
            break
        imGray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)  
        #cv.imshow("Original video", im)
        #cv.imshow("Gray video", imGray)

        imagesArrayGray[fc] = imGray
        cv.imshow('test numpy array display', imagesArrayGray[fc])

        fc += 1

        # Look for pollKey documentation
        key = cv.pollKey()

    meanImage = calculateAverageImages(400, imagesArrayGray, videoWidth, videoHeight)
    cv.imshow('Mean image', meanImage)

    # Détection de la route
    resRoad = detectRoad(meanImage, imagesArrayGray, 22, videoWidth, videoHeight, 50)
    
    # Détection des voitures
    resCars = detectCars(meanImage, imagesArrayGray, 200, videoWidth, videoHeight, 50)
    
    # Affichage de la séquence des voitures détectées
    cv.namedWindow('Cars Detection')
    for i in range(len(resCars)):
        cv.imshow('Cars Detection', resCars[i])
        key = cv.waitKey(int(1000/fps))
        if key == ESC_KEY or key == Q_KEY:
            break

    cv.waitKey(10000)

    # release cap
    cap.release()
    # Destroying all OpenCV windows
    cv.destroyAllWindows()
    

if __name__ == "__main__":
    main()
