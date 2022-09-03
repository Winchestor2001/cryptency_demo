window.onload = () => {
    let loader = document.querySelector('#preloader');
    let tanirovka = document.querySelector('.tanirovka');
    loader.style.opacity = 0;
    loader.style.visibility = 'hidden';
    tanirovka.style.opacity = 0;
    tanirovka.style.visibility = 'hidden';
};

let get_file = document.querySelector(".get_file");
let get_file_input = document.querySelector("#get_file_input");
get_file.addEventListener("click", function () {
  get_file_input.click();
});
function clickInput() {
  let send_file_btn = document.querySelector("#send_ava");
  send_file_btn.submit();
}
const toastTrigger = document.querySelectorAll(".liveToastBtn");
const toastLiveExample = document.getElementById("liveToast");
const toastbody = document.querySelector(".toast-body");
if (toastTrigger) {
  toastTrigger.forEach((item) => {
    item.addEventListener("click", () => {
      const copyText = item.getAttribute("data-link");
      if (copyText) {
        if (copyText == "none") {
          console.log(toastbody);
          toastbody.innerHTML = "У вас еще нет реф.ссылки";
        } else {
          console.log(toastbody);
          navigator.clipboard.writeText(copyText).then(() => {
            toastbody.innerHTML = "Реф.ссылка скопирована";
          });
        }
      }
      const toast = new bootstrap.Toast(toastLiveExample);

        toast.show();
    });
  });
}

const btns = document.querySelectorAll(".tab-btn");

const btn_header = document.getElementById("btn_header");

btn_header.addEventListener("click", () => {
  left_content.classList.toggle("active");
});

const setBtn = document.querySelectorAll(".sett-btn");
const articles1 = document.querySelectorAll(".content1");
const setting = document.querySelector(".mySettings");
let left_content = document.querySelector(".left_content");

setting.addEventListener("click", function (e) {
  const id = e.target.dataset.bsTarget;
  if (id) {
    e.target.classList.add("active");
    articles1.forEach(function (article) {
      article.classList.remove("active");
    });
    const element = document.getElementById(id);
    element.classList.add("active");
  }
});
