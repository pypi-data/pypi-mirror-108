
import json
import asyncio
import os
import sys
import re

import numpy as np
import cv2 as cv

from os import path

from _sliceFrames import CFRAndSliceList, ConvertToSDCFR, CFRAndSliceList

#CFRAndSliceList(HDvideoName, args["framerate"], args["slicerateHD"], HDFolder)
#ConvertToSDCFR(HDvideoName, args["framerate"], args['bitrateSD'], SDvideoName)
#CFRAndSliceList(SDvideoName, args["framerate"], args["slicerateSD"], SDFolder)

def GetSAD(frame1, frame2):
    dif = cv.absdiff(frame1[int(frame1.shape[0] / 8):int(7 * frame1.shape[0] / 8)],
                     frame2[int(frame2.shape[0] / 8):int(7 * frame2.shape[0] / 8)])
    sad = cv.mean(dif)  # sum(dif)/(frame1.shape[0]*frame1.shape[1]);
    return sad

def get_scene_changes(videofilename):
    idx = []
    sads = []
    cap = cv.VideoCapture()
    cap.setExceptionMode(False)
    if not cap.open(videofilename):
        print('Failed opening file: ' + str(videofilename))
        cap.release()
        return idx, sads
    cnt = 0
    prevFrame = None
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            # print("Can't receive frame (stream end?). Exiting ...")
            break
        ts = cap.get(cv.CAP_PROP_POS_MSEC)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        if prevFrame is None:
            prevFrame = gray
        sad = GetSAD(gray, prevFrame)
        if sad[0] > 40:
            print ('scene change at cnt: '+str(cnt))
            idx.append(cnt)
            sads.append(sad[0])
            #cv.imwrite('scene_frame_%04d.png' % cnt, frame)
            #cv.imshow('prev frame' +str(cnt), prevFrame)
            #cv.imshow('new frame ' +str(cnt) + ", SAD " + str(sad[0]), gray)
            #cv.waitKey(0)
            #cv.destroyAllWindows()
        prevFrame = gray
        cnt += 1

    cap.release()
    print('Processed file ' + videofilename + ' for scene changes')
    # print sads
    return idx, sads

def get_frames_framerate(videofilename, framerate):
    cap = cv.VideoCapture()
    cap.setExceptionMode(False)
    if not cap.open(videofilename):
        print('Failed opening file: ' + videofilename)
        cap.release()
        return

    print('Total nr of frames: '+ str(int(cap.get(cv.CAP_PROP_FRAME_COUNT ))))
    print('Frame rate: ' + str(cap.get(cv.CAP_PROP_FPS)))
    print('Frame size: ' + str(int(cap.get(cv.CAP_PROP_FRAME_WIDTH)))+' x '+str(int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

    if framerate == 0:
        print('Expected nr of frames to be processed: ' + str(int(cap.get(cv.CAP_PROP_FRAME_COUNT ))))
    else:
        print('Expected nr of frames to be processed: ' + str(int(cap.get((cv.CAP_PROP_FRAME_COUNT)/cap(cv.CAP_PROP_FPS))*framerate)))

    dt = 0.0
    if framerate > 0:
       dt = 1000/framerate

    imagefiles = list(filter(lambda f: f.endswith(('.jpg')), os.listdir(os.path.join(os.getcwd(),"images"))))
    imagefiles.sort(key=lambda var: [int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

    # determine first count
    cnt = 1

    if len(imagefiles) > 0:
        lastimage = os.path.splitext(imagefiles[len(imagefiles)-1])[0]
        cnt = int(lastimage[2:len(lastimage)])+1

    prevts = 0.0

    im = './images/im%06d.jpg'
    while cap.isOpened():
         ret, frame = cap.read()

         # if frame is read correctly ret is True
         if not ret:
            # print("Can't read frame Exiting ...")
            break
         ts = cap.get(cv.CAP_PROP_POS_MSEC)

         if framerate == 0:
             cv.imwrite(im % cnt, frame)
         else:
             if cnt == 0:
                 cv.imwrite(im % cnt, frame)
                 prevts = ts
             elif ts - prevts >= dt:
                cv.imwrite(im % cnt, frame)
                prevts = ts

         cnt += 1

    cap.release()
    print('Processed frames of file ' + videofilename)
    return

def get_frames(videofilename, idxs):
    cap = cv.VideoCapture()
    cap.setExceptionMode(False)
    if not cap.open(videofilename):
        print('Failed opening file: ' + videofilename)
        cap.release()
        return

    print('Total nr of frames: '+ str(int(cap.get(cv.CAP_PROP_FRAME_COUNT))))
    print('Frame rate: ' + str(cap.get(cv.CAP_PROP_FPS)))
    print('Frame size: ' + str(int(cap.get(cv.CAP_PROP_FRAME_WIDTH))) + ' x '+str(int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

    cnt = 0
    imagefiles = list(filter(lambda f: f.endswith(('.jpg')), os.listdir(os.path.join(os.getcwd(),"images"))))
    imagefiles.sort(key=lambda var: [int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

    j = 0

    file =  os.path.splitext(videofilename)[0]
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
#           print("Can't read frame Exiting ...")
            break
        if cnt == idxs[j]:
            ts = cap.get(cv.CAP_PROP_POS_MSEC)
            cv.imwrite("./images/im" + '%06d.jpg' % cnt, frame)
            j += 1
            if j == len(idxs):
                break
        cnt += 1

    cap.release()
    print('Processed frames of file ' + videofilename)
    return

def get_images_framerate(file_name, framerate):
    # extract image files from frames: framerate 0 is all frames
    get_frames_framerate(file_name, framerate)

def get_images(file_name):
    sads = []
    idxs = []

    # get list of scene changes based on sad calculation
    idxs, sads = get_scene_changes(file_name)

    # add the first frame
    idxs.insert(0,0)

    frs = []
    cnt = 0

    mindist = 20
    maxFrames = 10

    # selecting key frames based on scene changes
    while cnt < len(idxs)-1:
        frs.append(idxs[cnt])
        diff = idxs[cnt+1] - idxs[cnt]

        incr = diff / maxFrames

        if incr < mindist:
            incr = mindist

        if int(incr) > 0:
            for i in range(1,maxFrames-1):
                frame = idxs[cnt]+int(i*incr)
                if frame < idxs[cnt+1]:
                    frs.append(frame)
        cnt += 1
    frs.append(idxs[cnt])

    # extract image files from selected key frames
    get_frames(file_name, frs)