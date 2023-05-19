import cv2
import dlib
import face_recognition
import pandas as pd

# Load the pre-trained face detection model
detector = dlib.get_frontal_face_detector()

# Load the pre-trained face recognition model
known_faces = []
known_names = []

# Load the student database and train the face recognition model
student_data = pd.read_csv('student_database.csv')
for i in range(len(student_data)):
    name = student_data.iloc[i]['Name']
    image = cv2.imread(student_data.iloc[i]['Image'])
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    known_faces.append(face_encodings[0])
    known_names.append(name)

# Open the video stream using Agora SDK
# Replace <APP_ID> and <TOKEN> with your Agora app ID and token
agora_client = AgoraRTC.createClient()
agora_client.init("<APP_ID>")
agora_client.join("<TOKEN>", "<CHANNEL>", None)

# Initialize the attendance record
attendance_record = {name: 'Absent' for name in known_names}

# Start capturing frames from the video stream
while True:
    # Capture a frame from the video stream
    frame = agora_client.captureFrame()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    faces = detector(gray, 0)
    
    # Loop through each detected face
    for face in faces:
        # Get the face encoding
        encoding = face_recognition.face_encodings(frame, [face])[0]
        
        # Compare the face encoding with the known encodings
        matches = face_recognition.compare_faces(known_faces, encoding)
        
        # If a match is found, mark the corresponding student as present
        if True in matches:
            index = matches.index(True)
            name = known_names[index]
            attendance_record[name] = 'Present'
            
    # Display the processed frame
    cv2.imshow('frame', frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close the window
agora_client.release()
cv2.destroyAllWindows()

# Save the attendance record to a CSV file
attendance_data = pd.DataFrame.from_dict(attendance_record, orient='index', columns=['Attendance'])
attendance_data.to_csv('attendance_record.csv')
