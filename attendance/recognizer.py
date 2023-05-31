import cv2
import numpy as np
import joblib
import keras
import os 
# Load the model

# Load the model
m = keras.models.load_model('/home/nishad/Mine/Development/SPL-3/FinalProject/SpectaX/attendance/packages/face_recognizer_model.h5')


# Load the pre-trained face detection model
model_path = "/home/nishad/Mine/Development/SPL-3/FinalProject/SpectaX/attendance/packages/opencv_face_detector.pbtxt"  # Update with the path to your face detection model
model_config = "/home/nishad/Mine/Development/SPL-3/FinalProject/SpectaX/attendance/packages/deploy.prototxt"  # Update with the path to your model configuration file
model_weights = "/home/nishad/Mine/Development/SPL-3/FinalProject/SpectaX/attendance/packages/res10_300x300_ssd_iter_140000.caffemodel"  # Update with the path to your model weights file
net = cv2.dnn.readNetFromCaffe(model_config, model_weights)


def preprocess_and_detect_faces(image):
    # Construct an input blob for the network
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)

    # Set the input blob for the network
    net.setInput(blob)

    # Run forward pass to perform face detection
    detections = net.forward()

    # Iterate over the detected faces
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections with a confidence threshold
        if confidence > 0.5:
            # Get the bounding box coordinates of the face
            box = detections[0, 0, i, 3:7] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])
            (x, y, w, h) = box.astype("int")

            # Crop the face region from the original image
            face = image[y:y + h, x:x + w]

            # Perform any additional preprocessing steps if needed
            face = cv2.resize(face, (224, 224))
            face = face / 255.0
            face = np.expand_dims(face, axis=0)
            # Return the preprocessed face
            return face
    # If no faces are detected, return None
    return None


def predict(image_path):
    # image_path = "/home/nishad/Mine/Development/SPL-3/FinalProject/SpectaX/attendance/img.jpg"  # Update with the path to your image file
    #output_path = "preprocessed_face.jpg"  # Update with the desired output path

    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # image_path = os.path.join("/home/nishad/Mine/Development/SPL-3/FinalProject/SpectaX", str(image_path))
    print("Image is received....!!")
    processed_image = preprocess_and_detect_faces(cv2.imread(image_path))



    # Make prediction using the model
    if processed_image is None:
        print("No image is found!")
    else:
        predictions = m.predict(processed_image)
        predicted_labels = np.argmax(predictions, axis=1)

        # labels = {0: 'ASH1825003', 1:'1825005M', 2:'1825007M', 3:'1825013F', 4:'1825030M', 5:'1825029M', 6:'1825030', 7:'1825036M'}
        labels = {2:'1825007M', 4:'1825029M', 7:'1825036M'}
        if int(predicted_labels) in labels:
            print("Person:", labels[int(predicted_labels)])
        else:
            print("Unknown!!")
        recognized_person = labels[int(predicted_labels)]

        return recognized_person

# Get the saved image path
