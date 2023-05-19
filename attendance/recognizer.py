from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib

import face_recognition
import numpy as np
import cv2
import os
from datetime import datetime


# Attentiveness detection ------------------>
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


# Threshold value which suggests closed eyes
thresh = 0.27
# Checking for some n frames
frame_check = 20
# Detect face
detect = dlib.get_frontal_face_detector()
# Dat file is the crux of the code
predict = dlib.shape_predictor(
    "/home/nishad/Mine/Development/SPL-3/FinalProject/SpectaX/attendance/data/shape_predictor_68_face_landmarks.dat")

# Getting the start and end points for both eyes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

# Ends ------------------------------------>


def Recognizer(details):

    # path = ""

    base_dir = os.path.dirname(os.path.abspath(__file__))
    # os.chdir("..")
    base_dir = os.getcwd()
    path = os.path.join(base_dir, "{}/{}/{}/{}".format('static', 'images',
                        'Student_Images', details['session']))
    # print(image_dir)

    images = []
    classNames = []
    names = []
    MyList = os.listdir(path)
    print(MyList)
    for cls in MyList:
        currentimage = cv2.imread(f'{path}/{cls}')
        images.append(currentimage)
        classNames.append(os.path.splitext(cls)[0])

    print(classNames)

    def findEncoding(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode_img = face_recognition.face_encodings(img)[0]
            encodeList.append(encode_img)

        return encodeList

    knownImg_encodeList = findEncoding(images)

    print("Encodding Complete")

    def markAttendance(name):
        with open('/home/nishad/Desktop/test/Attendance.csv', 'r+') as f:
            myDataList = f.readlines()

            # print(myDataList)
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')

    cap = cv2.VideoCapture(0)
    flag = 0
    attn = 1
    total_frame = 0
    attentive_frame = 0
    while True:

        success, img = cap.read()
        total_frame += 1

        # Recognize starts ---------------------->
        if success == True:
            imgResize = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgResize_RGB = cv2.cvtColor(imgResize, cv2.COLOR_BGR2RGB)

            face_Currentframe = face_recognition.face_locations(imgResize_RGB)
            encode_Currentframe = face_recognition.face_encodings(
                imgResize_RGB, face_Currentframe)

            for encodeface, faceLoc in zip(encode_Currentframe, face_Currentframe):
                matches = face_recognition.compare_faces(
                    knownImg_encodeList, encodeface)
                faceDis = face_recognition.face_distance(
                    knownImg_encodeList, encodeface)

                if min(faceDis) < 0.45:
                    matchIndex = np.argmin(faceDis)
                    if matches[matchIndex]:
                        name = classNames[matchIndex].upper()

                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2-35), (x2, y2),
                                      (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        markAttendance(name)

                        if name not in names:
                            names.append(name)
                        # print(names)

                        # cap.release()
                        # cv2.destroyAllWindows()
                        # print("Names are:", names)
                        # return names

            # Recognize ends --------------------->
            # Attentivenes Starts ------------------>
            GAZE = 'Face not detected'
            img = imutils.resize(img, width=450)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            subjects = detect(gray, 0)
            txt = 'Not Attentive'
            for subject in subjects:
                structure = predict(gray, subject)
                # converting to NumPy Array
                structure = face_utils.shape_to_np(structure)
                # Draw rectangle for face detection
                if subjects != []:
                    for subject in subjects:
                        x = subject.left()
                        y = subject.top()
                        w = subject.right() - x
                        h = subject.bottom() - y
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        txt = 'Attentive'
                        attentive_frame += 1
                        GAZE = ''

                leftEye = structure[lStart:lEnd]
                rightEye = structure[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0
                # Bordering eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(img, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(img, [rightEyeHull], -1, (0, 255, 0), 1)
                if ear < thresh:
                    flag += 1
                    if flag >= frame_check:
                        cv2.putText(img, "********DROWSINESS DETECTED!**********", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        # print ("Drowsy")
                        txt = 'Not Attentive'
                else:
                    flag = 0
            cv2.putText(img, GAZE, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(img, txt, (10, 325),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # cv2.imshow("Frame", img)

            # Attentiveness ends -------------------->

            cv2.imshow('Webcam', img)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Names are:", names)

    print(total_frame)
    print(attentive_frame)
    print("Attentiveness in percentage: ",(attentive_frame/total_frame)*100)
    return names
