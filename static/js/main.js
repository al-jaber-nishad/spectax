
// // Toogle Button 
// let sideBar = document.getElementById("sidebar");
// let mainContent = document.getElementById("main-content");

// const btn = document.getElementById("toggle-btn")

// btn.addEventListener('click', toggle)

// function toggle() {
//   console.log("clicked")
// }

// console.log(btn)


// // btn.onclick = () => {
// //   console.log('btn clicked')
// //   sideBar.classList.toggle("sidebar-inactive");
// //   mainContent.classList.toggle("main-content-inactive")
// // }




// function openNav() {
// document.getElementById("sidebar").style.width = "215px";
// document.getElementById("main-content").style.marginLeft = "250px";
// }

// function closeNav() {
// document.getElementById("sidebar").style.width = "70px";
// document.getElementById("main-content").style.marginLeft= "70px";
// }




// Get the sidebar element
var sidebar = document.getElementById("sidebar");

// Get the button that opens the sidebar
var toggleBtn = document.getElementById("toggle-btn");

// Function to toggle the sidebar
function toggleSidebar() {
    if (sidebar.style.display === "none") {
        sidebar.style.display = "block";
    } else {
        sidebar.style.display = "none";
    }
}
