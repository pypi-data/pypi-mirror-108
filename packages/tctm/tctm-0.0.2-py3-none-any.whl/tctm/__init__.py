"""
Face Detect
By: Henry
"""

import cv2
import mediapipe as mp


class FaceDetector:
    def __init__(self, detectionCon=0.5):
        self.detectionCon = detectionCon
        self.mpFaces = mp.solutions.face_detection
        self.faces = self.mpFaces.FaceDetection(self.detectionCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFmesh = mp.solutions.face_mesh
        self.fmesh = self.mpFmesh.FaceMesh()
        self.mpHand = mp.solutions.hands
        self.hand = self.mpHand.Hands()

    def findFaces(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faces.process(imgRGB)
        if self.results.detections:
            for d in self.results.detections:
                box = d.location_data.relative_bounding_box
                h, w, c = img.shape
                x = int(box.xmin * w)
                y = int(box.ymin * h)
                width = int(box.width * w)
                height = int(box.height * h)
                return (x,y,width,height)

    def findHand(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hand.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for d in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, d, self.mpHand.HAND_CONNECTIONS)
        return img

    def findFace(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.fmesh.process(imgRGB)
        if self.results.multi_face_landmarks:
            for d in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,d,self.mpFmesh.FACE_CONNECTIONS)
        return img


d = FaceDetector(detectionCon=0.5)


def detectFace(img):
    return d.findFace(img)


def detectHand(img):
    return d.findHand(img)


def main():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        img = detectFace(img)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()