function openTrailer(){
document.getElementById("trailerModal").style.display="block";
}

function closeTrailer(){
document.getElementById("trailerModal").style.display="none";
}

document.querySelectorAll(".gallery img").forEach(img => {

img.onclick = () => {

let viewer = document.createElement("div");

viewer.className = "image-viewer";

viewer.innerHTML = `<img src="${img.src}">`;

document.body.appendChild(viewer);

viewer.onclick = () => viewer.remove();

};

});