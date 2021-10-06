#!/usr/bin/env python3
import copy
import numpy as np
import cv2
class TrackVision():
    def __init__(self):
        self.pyrDown = 0

    def draw_grid(self,rows,cols,step,sceneDetected):
        gap_y = rows // step
        gap_x = cols // step
        for i in range(step):
            cv2.line(sceneDetected, (0, i * gap_y), (cols, i * gap_y), (0,255,255),1 )
        for j in range(step):
            cv2.line(sceneDetected, (j * gap_x, 0), (j * gap_x, rows), (0,255,255),1 )
        maskBlack = np.ones(sceneDetected.shape[:2], dtype="uint8") * 255
        for i in range(step):
            for j in range(step):
                sub_image = sceneDetected[j*gap_y:j*gap_y+gap_y, i*gap_x:i*gap_x+gap_x]
                sum=np.sum(sub_image==0)
                if(np.sum(sub_image==0)>137):
                    maskBlack = np.ones(sceneDetected.shape[:2], dtype="uint8") * 255
                    maskVehicleBoxTopLeftXY = (i*gap_x,j*gap_y)
                    maskVehicleBoxBottomRightXY = (i*gap_x+gap_x,j*gap_y+gap_y)
                    maskVehicle = cv2.rectangle(maskBlack,maskVehicleBoxTopLeftXY,maskVehicleBoxBottomRightXY,color=0,thickness=-1)
                    sceneDetected=cv2.bitwise_and(sceneDetected,sceneDetected,mask=maskVehicle)
        return sceneDetected



        
    def pixyImageCallback(self, scene):
        scenePyr = copy.deepcopy(scene)
        if self.pyrDown > 0:
            for i in range(self.pyrDown):
                scenePyr = cv2.pyrDown(scenePyr)
        sceneDetect = copy.deepcopy(scenePyr)
        rows,cols,channel=sceneDetect.shape
        print(rows,cols)
        passedImageGray = cv2.cvtColor(sceneDetect,cv2.COLOR_BGR2GRAY)
        sceneDetected = (cv2.threshold(
            passedImageGray, 200, 255, cv2.THRESH_BINARY)[1])
        step = 10
        sceneDetected=self.draw_grid(rows,cols,step,sceneDetected)
        # ret, corners = cv2.findChessboardCorners(sceneDetected, (10,10), None)
        # print(corners)
        # cv2.drawChessboardCorners(sceneDetected, (7,6), corners, ret)
        cv2.imshow('sceneDetected', sceneDetected)
        print(len(sceneDetected))
        cv2.waitKey(0)




def main():
    node = TrackVision()
    img=cv2.imread("track.png")
    node.pixyImageCallback(img)


if __name__ == '__main__':
    main()