#これが新しいメイン
#python3 Start.pyで実行
import numpy as np
import cv2
from cv2 import aruco
import multiprocessing
from EdeskModule.canvaslib import Canvas
from EdeskModule.cameralib import Camera
from EdeskModule.detectorlib import YoloDetector,ArucoDetector
from EdeskModule.contentlib import ContentManager

from multiprocessing import RawArray,Process
from time import perf_counter
import ctypes

class Main:
    #Parameter for Realsense
    #USB3.1のときは1280x720まで可能，USB抜き差しでうまく3.1で認識させること または640x480
    width_realsense=1280
    height_realsense=720
    fps_realsense=30

    padding_projector=80
    colorBuffer=None
    depthBuffer=None
    colorMat=None
    depthMat=None

    camera=None
    def __init__(self):
        self.setup()
        pass
    def setup(self):
        self.canvas=Canvas()
        self.camera=Camera(self.width_realsense,self.height_realsense,self.fps_realsense)
        self.cameraBufferLength=self.width_realsense*self.height_realsense*3
        
        self.colorMat=np.zeros((self.height_realsense,self.width_realsense,3),dtype=np.uint8)
        npDepthBuffer=np.zeros((self.height_realsense,self.width_realsense,3),dtype=np.uint8)
        
        ctypesColorBuffer=self.colorMat.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8*self.cameraBufferLength)).contents
        ctypesDepthBuffer=npDepthBuffer.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8*self.cameraBufferLength)).contents
        
        self.colorBuffer=RawArray('B',ctypesColorBuffer)
        self.depthBuffer=RawArray('B',ctypesDepthBuffer)
        
        self.camera.setColorBuffer(self.colorMat)
        cameraProcess=Process(target=self.camera.process,args=[self.colorBuffer])
        cameraProcess.start()
        pass
    def update(self):
        vec=np.ctypeslib.as_array(self.colorBuffer)
        mat=vec.reshape(self.height_realsense,self.width_realsense,3)
        cv2.imshow("color",mat)
        cv2.waitKey(1)
        pass
    def buffer2cvmat(self):
        ndcolor=np.array(self.colorBuffer,dtype=np.uint8)
        self.colorMat=ndcolor.reshape((self.height_realsense,self.width_realsense,3))
        nddepth=np.array(self.depthBuffer,dtype=np.uint8)
        self.depthMat=nddepth.reshape((self.height_realsense,self.width_realsense,3))        
        pass
    pass



if __name__ == "__main__":
    main=Main()

    while True:
        stime=perf_counter()
        main.update()
        etime=perf_counter()
        print("Main time:",etime-stime)
    pass
