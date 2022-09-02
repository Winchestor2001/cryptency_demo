let videos_section = document.querySelector(".videos_section");
let video_card = document.querySelectorAll(".video_card");
let intro = document.querySelector(".intro");
video_card.forEach((item) => {
    item.addEventListener("click", function () {
        item.children[0].style.display = "none";
    });
});