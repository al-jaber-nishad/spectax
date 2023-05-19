
const APP_ID = "3b8715d70eb24308b4bb45a28bce1249";
const TOKEN = sessionStorage.getItem("token");
const CHANNEL = sessionStorage.getItem("room");
let UID = sessionStorage.getItem("UID");

let NAME = sessionStorage.getItem("name");

const client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });

let localTracks = await AgoraRTC.createMicrophoneAndCameraTracks();
await client.publish([localTracks[0], localTracks[1]]);



client.on("user-published", async (user, mediaType) => {
  remoteUsers[user.uid] = user;
  await client.subscribe(user, mediaType);

  if (mediaType === "video") {
    let player = document.getElementById(`user-container-${user.uid}`);
    if (player != null) {
      player.remove();
    }

    let member = await getMember(user);

    player = `<div  class="video-container" id="user-container-${user.uid}">
            <div class="video-player" id="user-${user.uid}"></div>
            <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
        </div>`;

    document
      .getElementById("video-streams")
      .insertAdjacentHTML("beforeend", player);
    user.videoTrack.play(`user-${user.uid}`);

    // Create a canvas element to capture the video frames
    let canvas = document.createElement("canvas");
    canvas.width = user.videoTrack.track.width;
    canvas.height = user.videoTrack.track.height;
    canvas.style.display = "none";
    document.body.appendChild(canvas);

    // Use the canvas to capture each frame of the video stream
    let ctx = canvas.getContext("2d");
    setInterval(() => {
      ctx.drawImage(
        user.videoTrack.track,
        0,
        0,
        canvas.width,
        canvas.height
      );
      let imageData = canvas.toDataURL("image/png");
      // Send the imageData to your Django backend for face recognition
      console.log("sent frame")
    }, 1000 / 30); // 30 frames per second
  }
});




let leaveAndRemoveLocalStream = async () => {
  for (let i = 0; localTracks.length > i; i++) {
    localTracks[i].stop();
    localTracks[i].close();
  }

  await client.leave();
  //This is somewhat of an issue because if user leaves without actaull pressing leave button, it will not trigger
  deleteMember();
  window.open("/", "_self");
};


document
  .getElementById("leave-btn")
  .addEventListener("click", leaveAndRemoveLocalStream);
document.getElementById("camera-btn").addEventListener("click", toggleCamera);
document.getElementById("mic-btn").addEventListener("click", toggleMic);