import face_recognition     # main algorithm
import pickle               # deserialize data
import cv2                  # opencv, image processment
import faiss
import numpy as np
#import pandas as pd
import os

def generate_encodings():
    path = "../dataset/"
    imagePaths = []
    for i in os.listdir(path):
        print("[INFO] reading {} folder".format(i))
        if i != ".DS_Store":
            for j in os.listdir(path+i):
                imagePaths.append(path+i+"/"+j)
    '''
    output from imagePaths:
    '[./dataset/pedro/pedro1.jpeg',
    './dataset/pedro/pedro2.jpeg',
    './dataset/pedro/pedro3.jpeg',
    './dataset/joe/joe3.jpeg',
    './dataset/joe/joe4.jpeg',
    './dataset/joe/joe2.webp',
    './dataset/joe/joe1.jpg']
    '''

    known_encodings = []
    known_names = []
    known_images = []

    for (i, imagePath) in enumerate(imagePaths):
        if (i+1) % 100 == 0:
            print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
        # name = imagePath.split(os.path.sep)[-2] #should work, but doesnt
        name = imagePath.split("/")[-2] #hotfix?
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # For 7 images. CNN = 22.7s and HOG = 1.6s
        boxes = face_recognition.face_locations(rgb, model="hog")
        
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(name)
            known_images.append(imagePath)

    print("[INFO] serializing encodings...")
    data = {"encodings": known_encodings, "names": known_names, "paths": known_images}
    # data = {'encodings': [array(128-d face vector], 'names': ['pedro', 'joe', 'joe', ..., 'pedro'])]}

    print(len(data['encodings']))
    print(len(data['names']))
    print(len(data['paths']))

    f = open("../encodings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()