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
window.onload = updateProgressBar;

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
  