window.onload = () => {
  let loader = document.querySelector("#preloader");
  let tanirovka = document.querySelector(".tanirovka");
  loader.style.opacity = 0;
  loader.style.visibility = "hidden";
  tanirovka.style.opacity = 0;
  tanirovka.style.visibility = "hidden";
};

const modal1 = document.getElementById("myModal1");
const inp1 = document.getElementById("inp1");
const click1 = document.getElementById("click1");
const span1 = document.getElementById("close1");
const chek1 = document.getElementById("chek1");
const modal2 = document.getElementById("myModal2");
const inp2 = document.getElementById("inp2");
const click2 = document.getElementById("click2");
const span2 = document.getElementById("close2");
const chek2 = document.getElementById("chek2");
const btn = document.getElementById("submit");

inp1.addEventListener("click", () => {
  if (inp1.checked == true) {
    modal1.style.display = "block";
    return;
  }
  disabledBtn();
});
span1.addEventListener("click", () => {
  checkBoxes(inp1, chek1, modal1);
  disabledBtn();
});
click1.addEventListener("click", () => {
  checkBoxes(inp1, chek1, modal1);
  disabledBtn();
});
inp2.addEventListener("click", () => {
  if (inp2.checked == true) {
    modal2.style.display = "block";
    return;
  }
  disabledBtn();
});
span2.addEventListener("click", () => {
  checkBoxes(inp2, chek2, modal2);
  disabledBtn();
});
click2.addEventListener("click", () => {
  checkBoxes(inp2, chek2, modal2);
  disabledBtn();
});

window.onclick = function (event) {
  if (event.target == modal1) {
    checkBoxes(inp1, chek1, modal1);
    disabledBtn();
  }
  if (event.target == modal2) {
    checkBoxes(inp2, chek2, modal2);
    disabledBtn();
  }
};
function checkBoxes(inp, chek, modal) {
  if (chek.checked == false) {
    inp.checked = false;
    modal.style.display = "none";
    return;
  }
  inp.checked = true;
  modal.style.display = "none";
  chek.checked = false;
}
function disabledBtn() {
  if (inp1.checked == true && inp2.checked == true) {
    btn.disabled = false;
  } else {
    btn.disabled = true;
  }
}

let input1 = document.querySelector(".password1");
let input2 = document.querySelector(".password2");
let btn1 = document.querySelector("#pass1");
let btn2 = document.querySelector("#pass2");

let arr = [btn1, btn2];
arr.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (input1.type == "password") {
      input1.type = "text";
      input2.type = "text";
      btn1.children[0].classList.add("fa-eye-slash");
      btn1.children[0].classList.remove("a-eye");
      btn2.children[0].classList.add("fa-eye-slash");
      btn2.children[0].classList.remove("a-eye");
    } else {
      input1.type = "password";
      input2.type = "password";
      btn1.children[0].classList.remove("fa-eye-slash");
      btn1.children[0].classList.add("a-eye");
      btn2.children[0].classList.remove("fa-eye-slash");
      btn2.children[0].classList.add("a-eye");
    }
  });
});

let error = document.querySelector(".error");
let error1 = document.querySelector(".error1");
let input3 = document.querySelector(".password3");
input1.addEventListener("input", () => {
  if (
    input1.value.match(/^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])([a-zA-Z0-9]{8,})$/)
  ) {
    // console.log(input1.value);
    // console.log('True');
    error.classList.add("dNone");
    input1.style.background = "#67e088";
  } else {
    error.classList.remove("dNone");
    input1.style.background = "#f76060";
    // console.log('Error');
  }
});
input2.addEventListener("input", () => {
  if (input2.value == input1.value) {
    error1.classList.add("dNone");
    input2.style.background = "#67e088";
  } else {
    error1.classList.remove("dNone");
    input2.style.background = "#f76060";
  }
});

input3.addEventListener("input", () => {
  if (
    input1.value.match(/^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])([a-zA-Z0-9]{8,})$/)
  ) {
    // console.log(input1.value);
    // console.log('True');
    error.classList.add("dNone");
    input3.style.background = "#67e088";
  } else {
    error.classList.remove("dNone");
    input3.style.background = "#f76060";
    // console.log('Error');
  }
});
