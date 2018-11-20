import cv2
from base_camera import BaseCamera
import pyzbar.pyzbar as pyzbar
import numpy as pn
from threading import Thread

class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def decodeDisplayImage(image,dataimage):
        barcodes = pyzbar.decode(dataimage)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            newsize = (w,h)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

            print barcode.data.decode("utf-8")
            img2 = cv2.imread('bz.jpg')
            img2_out = cv2.resize(img2,newsize)
            rows1, cols1, channels1 = image.shape
            rows, cols, channels = img2_out.shape
            roi = image[y:(rows+y), x:(cols+x)]

            img2gray = cv2.cvtColor(img2_out, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)

            img1_bg = cv2.bitwise_and(roi, roi, mask=mask)
            img2_fg = cv2.bitwise_and(img2_out, img2_out, mask=mask_inv)

            dst = cv2.add(img1_bg, img2_fg)
            image[y:(rows+y), x:(cols+x)] = dst

        return image

    @staticmethod
    def decodeDisplay(image):
        barcodes = pyzbar.decode(image)

        for barcode in barcodes:

            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 125), 2)

        return image

    @staticmethod
    def frames():
        cv2.useOptimized()
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            try:
                # read current frame
                _, img = camera.read()
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                im = Camera.decodeDisplayImage(img,gray)
                # encode as a jpeg image and return it
                yield cv2.imencode('.jpg', im)[1].tobytes()
            except Exception as e:
                print e
