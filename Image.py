# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 09:20:49 2020

@author: Kairav Patel
"""

import cv2 as cv
import numpy as np
import pyqt
import datetime
import torch


def Image(image):
    frame = cv.imread(image)
    frame = cv.resize(frame, (416, 416))
    return frame


def net(image, cfg, weight, response):
    image = Image(image)
    net = cv.dnn_DetectionModel(cfg, weight)
    if response == True:
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
    else:
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    net.setInputSize(832, 832)
    net.setInputScale(1.0 / 255)
    net.setInputSwapRB(True)

    start_time = datetime.datetime.now()
    classes, confidences, boxes = net.detect(
        image, confThreshold=0.5, nmsThreshold=0.5)
    end_time = datetime.datetime.now()
    infer_time = (end_time - start_time).total_seconds()
    detection = np.hstack((classes, confidences, boxes))
    return detection, infer_time


def plot_image(image, cfg, weight, response):
    #frame = Image(image)
    detection, time = net(frame, cfg, weight, response)
    no_faces = 0
    for detect in range(len(detection)):
        no_faces += 1
        box = detection[detect][2:]
        cv.rectangle(frame, box, color=(0, 255, 0), thickness=1)
    return frame, no_faces, time, detection


def save(image, time, detection):
    #cv.putText(image, str(time), (30, 20),
              # cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 1)
    cv.imwrite('output.jpg', image)
    txt = open('output.txt', 'a')
    for detect in range(len(detection)):
        box = detection[detect][2:]
        txt.write('Face' + " " + str(box) + "\n")
    txt.close()


def anonymize_face_pixelate(image, blocks=3):
    # Devide the iamge into the NXN Matrix
    (h, w) = image.shape[:2]
    xsteps = np.linspace(0, w, blocks+1, dtype='int')
    ysteps = np.linspace(0, h, blocks+1, dtype='int')
    # Loops over the all the boxes
    for i in range(1, len(xsteps)):
        for j in range(1, len(ysteps)):
            startx = xsteps[i-1]
            starty = ysteps[j-1]
            endx = xsteps[i]
            endy = ysteps[j]

            roi = image[starty:endy, startx:endx]
            (B, G, R) = [int(x) for x in cv.mean(roi)[:3]]
            cv.rectangle(image, (startx, starty), (endx, endy), (B, G, R), -1)
    return image


def blur(image, detection):
    frame = Image(image)
    frame_new = Image(image)
    for detect in range(len(detection)):
        box = detection[detect][2:]
        cv.rectangle(frame, box, color=(0, 255, 0), thickness=1)
        left, top, width, height = int(box[0]), int(
            box[1]), int(box[2]), int(box[3])
        face = frame[top:top+height, left:left+width]
        b_face = anonymize_face_pixelate(face, blocks=5)
        frame_new[top:top+height, left:left+width] = b_face
    return frame_new


def gpu():
    if torch.cuda.is_available():
        device = torch.cuda.current_device()
        return torch.cuda.is_available(), str(torch.cuda.get_device_name(device))
    else:
        return torch.cuda.is_available(), str('No')
