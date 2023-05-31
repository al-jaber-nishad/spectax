let videoStream = null; // Global variable to store the video stream

const startVideoStream = async () => {
  try {
    const video = document.getElementById("video-element");
    videoStream = await navigator.mediaDevices.getUserMedia({ video: true });

    // Attach the video stream to the video element
    video.srcObject = videoStream;
    video.play();

    console.log("Video stream started successfully!");
  } catch (error) {
    console.error("Error starting the video stream:", error);
  }
};

const stopVideoStream = () => {
  if (videoStream) {
    const videoTracks = videoStream.getVideoTracks();
    videoTracks.forEach((track) => track.stop());
    videoStream = null;

    console.log("Video stream stopped successfully!");
  }
};

const captureImage = async () => {
  try {
    if (!videoStream) {
      console.error("No video stream available.");
      return;
    }

    const canvas = document.createElement("canvas");
    const video = document.getElementById("video-element");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageBlob = dataURItoBlob(canvas.toDataURL("image/jpeg"));
    const formData = new FormData();
   
    
    // Get session data, course name, and period number from sessionStorage
    const session = sessionStorage.getItem("session");
    const course = sessionStorage.getItem("course");
    const period = sessionStorage.getItem("period");

    // Add session data, course name, and period number to the FormData object
    formData.append("image", imageBlob, "image.jpg");
    formData.append("session", session);
    formData.append("course", course);
    formData.append("period", period);


    // Send the image to the API using the Fetch API
    const response = await fetch("http://127.0.0.1:8000/api/upload-image/", {
      method: "POST",
      body: formData,
    });

    // Check the response status
    if (response.ok) {
      console.log("Image uploaded successfully!");
    } else {
      console.error("Failed to upload the image.");
    }
  } catch (error) {
    console.error("Error capturing and sending the image:", error);
  }
};

function dataURItoBlob(dataURI) {
  const byteString = atob(dataURI.split(",")[1]);
  const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  return new Blob([ab], { type: mimeString });
}

// Start the video stream
startVideoStream();

// Call the captureImage function every 5 seconds
setInterval(captureImage, 5000);

// Stop the video stream when necessary (e.g., when leaving the page)
// Call stopVideoStream() as needed
