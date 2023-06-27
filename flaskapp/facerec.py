import face_recognition     # main algorithm
import pickle               # deserialize data
import cv2                  # opencv, image processment
import faiss
import numpy as np
import pandas as pd

def detect_faces(img):
    data = pickle.loads(open("encodings.pickle", "rb").read())

    # Convert the image file to a NumPy array
    img_array = np.frombuffer(img, np.uint8)

    # Decode the image array to an OpenCV BGR image
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"
        if True in matches:
            matched_indexes = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matched_indexes:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            
            name = max(counts, key=counts.get)
            print("Found face: {}".format(name))
        names.append(name)

        for ((top, right, bottom, left), name) in zip(boxes, names):
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    f_str = "\n"
    for i in names:
        f_str += i + " "

    return f_str

def knn(img, k):
    r_data = pickle.loads(open("encodings.pickle", "rb").read())

    data = np.array(r_data['encodings'])
    d = data.shape[1]

    index = faiss.IndexFlatL2(d)
    index.add(data)

    img_array = np.frombuffer(img, np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)

    d = np.array([])

    for encoding in encodings:
        d = np.array([encoding])

    D, I = index.search(d, k) 
    #print(I)
    # I contains the indexes of the knn
    #n_data = pd.DataFrame(r_data['paths'])
    #print(n_data)

    images = []

    for i in I[0]:
        images.append("../"+r_data['paths'][i])

    print(images)
    return images