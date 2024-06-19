// Dapatkan elemen dengan id "question_now" dan "total_question"
var questionNowElement = document.getElementById("question_now");
var totalQuestionElement = document.getElementById("total_question");

// Dapatkan elemen .progress:after
var progressBarAfter = document.querySelector(".progress_orange");

// Fungsi untuk mengupdate lebar progress berdasarkan nilai question_now dan total_question
function updateProgressBar() {
  var questionNow = parseInt(questionNowElement.innerText);
  var totalQuestion = parseInt(totalQuestionElement.innerText);

  // Hitung persentase
  var percentage = (questionNow / totalQuestion) * 100;

  // Set lebar .progress:after sesuai persentase
  progressBarAfter.style.width = percentage + "%";
}

// Panggil fungsi saat halaman dimuat
window.addEventListener("load", updateProgressBar);

// animasi untuk memunculkan feedback
document.addEventListener("DOMContentLoaded", function () {
  var feedbackElement = document.getElementById("feedback");
  var feedbackText = feedbackElement.textContent; // Gunakan textContent bukan innerText
  feedbackElement.textContent = ""; // Gunakan textContent bukan innerText

  for (var i = 0; i < feedbackText.length; i++) {
    (function (index) {
      setTimeout(function () {
        feedbackElement.style.opacity = 1;
        feedbackElement.textContent += feedbackText[index]; // Gunakan textContent bukan innerText
        if (index === feedbackText.length - 1) {
          feedbackElement.textContent += " "; // Tambahkan spasi setelah semua kata selesai ditampilkan
        }
      }, 50 * index);
    })(i);
  }
});

// validate form

function validateForm() {
  let x = document.getElementById("answer").value;
  if (x == "") {
    alert("Kamu belum mengisi jawaban!!!");
    return false;
  } else {

    const submitContainer = document.querySelector('.submit-container');
    const submitButton = submitContainer.querySelector('input[type="submit"]');

    // Membuat elemen loader
    const loader = document.createElement('div');
    loader.classList.add('loader');

    // Mengganti tombol submit dengan loader
    submitContainer.removeChild(submitButton);
    submitContainer.appendChild(loader);
  }
}

//   for about page
document.querySelectorAll(".accordion-item").forEach((item) => {
  item.querySelector(".accordion-item-header").addEventListener("click", () => {
    item.classList.toggle("open");
  });
});

// for password confirmation 1
let result1;

function passConfirm1(arg){
  arg.addEventListener("input", (event) => {
    const username = document.getElementById("username_input").value;
    const password1 = document.getElementById("id_password1");
    const cond1 = document.getElementById("condition1");
    const cond2 = document.getElementById("condition2");
    const cond3 = document.getElementById("condition3");
    const passValue = password1.value;
  
    const [regex1, regex2, regex3] = [/^\w{8,}$/, /^\d+$/, new RegExp(username)];
  
    const regexes = [regex1, regex2, regex3];
    const [found1, found2, found3] = regexes.map(regex => regex.test(passValue));
  
    // Hapus semua kelas 'appro' sebelumnya
    [cond1, cond2, cond3].forEach((element) => {
      element.classList.remove("appro");
      element.classList.add("condition");
    });
    
    let resultCond1, resultCond2, resultCond3;

    // Tambahkan kelas 'appro' sesuai kondisi
    if (found1 && passValue.length) {
      cond1.classList.add("appro");
      cond1.classList.remove("condition");
      resultCond1 = true;
    } else {resultCond1 = false}
  
    if (!found2 && passValue.length) {
      cond2.classList.add("appro");
      cond2.classList.remove("condition");
      resultCond2 = true;
    } else {resultCond2 = false}
  
    if (!found3 && passValue.length) {
      cond3.classList.add("appro");
      cond3.classList.remove("condition");
      resultCond3 = true;
    } else {resultCond3 = false}

    result1 = resultCond1 && resultCond2 && resultCond3;
  });
}

passConfirm1(document.getElementById("id_password1"));

// for pass confirm 2
let result2;

function passConfirm2(arg){
  arg.addEventListener("input", (event) => {
    const password1 = document.getElementById("id_password1").value;
    const password2Raw = document.getElementById("id_password2");
    const password2 = password2Raw.value;
    const condPass1 = document.getElementById("passConfirm");
    const regex = new RegExp(password1);
    const found = regex.test(password2)
  
    condPass1.classList.remove("showElement")
    password2Raw.classList.remove("redBorder")
  
    if (!found && password2.length) {
      condPass1.classList.add("showElement")
      password2Raw.classList.add("redBorder")
      result2 = false;
    } else {result2 = true}
  })
};

passConfirm2(document.getElementById("id_password2"));

// for username valiadtion
let result3;

function userValid(arg){
  arg.addEventListener("input", (event) => {
    const username = document.getElementById("username_input").value;
    const userConfirm = document.getElementById("userConfirm");
    const regex = /\s/;
    const found = regex.test(username);
  
    userConfirm.classList.remove("showElement");
  
    if (found && username.length) {
      userConfirm.classList.add("showElement");
      result3 = false;
    } else {result3 = true};
  });
};

userValid(document.getElementById("username_input"));

// validate register form
function registValid(){
  if (!(result1 && result2 && result3)){
    alert("sepertinya masih ada yang salah atau belum terisi!");
    return false;
  } else {return true;}
}

// untuk validasi form pembuatan soal
function validateForm2() {
  const questInput = document.getElementById("questionInput").value;
  if (!questInput.length) {
    alert("sepertinya masih ada yang belum terisi");
    return false;
  }
}