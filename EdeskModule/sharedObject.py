import cv2
from cv2 import aruco
import multiprocessing
import numpy as np
from time import perf_counter
#どのプロセスでも共有したいデータをここに列挙
#ただし定数だけにすること
class Constants:
    DEBUG=True
    camera_width=1280
    camera_height=720
    camera_fps=30
    camera_length=camera_width*camera_height*3

    projector_padding=80
    projector_width=1920
    projector_height=1000
    projector_length=projector_height*projector_width*3

    canvas_width=projector_width-projector_padding*2
    canvas_height=projector_height-projector_padding*2
    canvas_length=canvas_height*canvas_width*3

    cameraID=4
    pass
class MyProcess(Constants):
    cameraColorMat=None
    cameraDepthMat=None
    yoloResult=None
    arucoResult=None
    canvasMat=None
    projectingMat=None
    def process(self,canvasBuffer,projectingBuffer,cameraColorBuffer,cameraDepthBuffer,arucoResult,yoloResult):
        #ここに引数のarrayとフィールドのmatの関連付け処理を入れる
        cvec=np.ctypeslib.as_array(canvasBuffer)
        self.canvasMat=cvec.reshape(self.canvas_height,self.canvas_width,3)

        pvec=np.ctypeslib.as_array(projectingBuffer)
        self.projectingMat=pvec.reshape(self.projector_height,self.projector_width,3)

        cvec=np.ctypeslib.as_array(cameraColorBuffer)
        self.cameraColorMat=cvec.reshape(self.camera_height,self.camera_width,3)

        dvec=np.ctypeslib.as_array(cameraDepthBuffer)
        self.cameraDepthMat=dvec.reshape(self.camera_height,self.camera_width,3)

        self.yoloResult=yoloResult
        self.arucoResult=arucoResult
        
        self.setup()
        while True:
            # stime=perf_counter()
            self.update()
            # etime=perf_counter()
            # print("Canvas.update:",etime-stime)
        pass
    def setup(self):
        print("warn:please override myprocess.setup")
        pass
    def update(self):
        print("warn:please override myprocess.update")
        pass
    