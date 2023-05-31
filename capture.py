import cv2

# Open the default camera (index 0)
camera = cv2.VideoCapture(0)

# Define a variable to keep track of the number of captured photos
photos_captured = 0

# Run a loop to capture 50 photos
while photos_captured < 50:
    # Read a frame from the camera
    ret, frame = camera.read()

    # Display the frame in a window
    cv2.imshow('Capture Photos', frame)

    # Wait for a key press
    key = cv2.waitKey(1)

    # If the 's' key is pressed, save the frame as an image
    if key == ord('s'):
        # Define the file name for the captured photo (you can modify the file name as per your preference)
        file_name = f'photo_{photos_captured}.jpg'

        # Save the frame as an image
        cv2.imwrite(file_name, frame)

        # Increment the count of captured photos
        photos_captured += 1
        print(f'Photo {photos_captured} captured!')

    # If the 'q' key is pressed, exit the loop
    elif key == ord('q'):
        break

# Release the camera and close the window
camera.release()
cv2.destroyAllWindows()
