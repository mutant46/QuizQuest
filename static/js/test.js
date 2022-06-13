const url = window.location.href;
const quizForm = document.querySelector("#quiz-form");
const quizBox = document.querySelector(".quiz-box");
const submit = document.querySelector("#submit");
const ResultBox = document.querySelector(".result-box");
const buttonBox = document.querySelector(".results");
const wrapper = document.querySelector(".test-wrapper");
const time = document.querySelector('#time').innerHTML.split(' ')[0];
let questions_data;
$.ajax({
  type: "GET",
  url: `${url}/data`,
  success: (response) => questions(response),
  error: (error) => console.log(error),
});


function questions(response) {
  questions_data = response.data;
  let ik;
  questions_data.forEach((el, i) => {
    for (const [question, answers] of Object.entries(el))
      [generate_html(question, answers, i)];
  });
}

function generate_html(question, answers, index) {
  quizBox.innerHTML += `
    <div class="question" style="margin-bottom : 6em">
        <h4 class="font-medium text-capitalize" id="quiz-question"> <span class="me-3 text-primary">Question-${
          index + 1
        } :</span>${question}</h4>
        <div class="options mt-3 d-flex justify-content-between">
            ${answers
              .map((answer) => {
                return `
                <div class="form-check option d-flex align-items-center mt-3 px-5">
                    <input class="form-check-input answer" type="radio" name="${question}" id="${question}" value="${answer}">
                    <label class="form-check-label ms-3" style="font-size :medium; font-weight : 500">
                        ${answer}
                    </label>
                </div>`;
              })
              .join("")}
        </div>   
        <hr>
    </div>`;
}

// Info : Prevent from copying
const disableselect = (e) => {  
  return false  
}  
document.onselectstart = disableselect  
document.onmousedown = disableselect

// Info : Manage Timer
const endtime = document.querySelector("#endtime")
const counter = document.querySelector('#timer')
var d1 = new Date ()
d1.setMinutes(d1.getMinutes() + parseInt(time) );
endtime.innerHTML = d1.toLocaleTimeString();
const timeInterval = setInterval(setTimer, 1000);
function setTimer() {
  const now = new Date();
  const distance = d1 - now;
  const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((distance % (1000 * 60)) / 1000);
  counter.innerHTML = `${minutes}:${seconds}`;
  if (distance < 0) {
    clearInterval(timeInterval);
    counter.innerHTML = "EXPIRED";
    submit.disabled = true;
    submit.classList.add("disabled");
    submit.classList.remove("btn-primary");
    submit.classList.add("btn-danger");
    submit.innerHTML = "Time Up";
    submit_quiz()
  }
}

    




const form = document.querySelector("#quiz-form");
const csrf = document.getElementsByName("csrfmiddlewaretoken");

const sendData = () => {
  const answers = [...document.getElementsByClassName("answer")];
  let data = {};
  data["csrfmiddlewaretoken"] = csrf[0].value;
  answers.forEach.call(answers, (ans) => {
    if (ans.checked) {
      data[ans.name] = ans.value;
    } else if (!data[ans.name]) {
      data[ans.name] = null;
    }
  });
  return data;
};

function showResults(response) {
  quizForm.classList.add("d-none");
  buttonBox.classList.remove("d-none");
  const results = response.results;
  const childCls = [
    "container-fluid",
    "p-3",
    "text-white",
    "mb-4",
    "font-weight-normal",
    "lh-lg",
  ];
  let i = 1;
  for (let x of results) {
    const questionBox = document.createElement("div");
    const number = document.createElement("h4");
    questionBox.classList.add(...childCls);
    const question = Object.keys(x)[0];
    number.innerHTML = `Question - ${i}`;
    ResultBox.appendChild(number);
    i++;

    if (x[question] == "not answered") {
      questionBox.innerHTML += `<p>quesiton : ${question}? | not answered</p>`;
      questionBox.classList.add("bg-danger");
    } else if (x[question].answerd == x[question].correct_answer) {
      questionBox.innerHTML += `<p><b>quesiton :</b> ${question}? <br> <b>you answerd : </b> ${x[question].answerd} <br> <b>correct :</b> ${x[question].correct_answer}</p>`;
      questionBox.classList.add("bg-success");
    } else {
      questionBox.innerHTML += `<p><b>quesiton :</b> ${question}? <br> <b>you answerd : </b> ${x[question].answerd} <br> <b>correct :</b> ${x[question].correct_answer}</p>`;
      questionBox.classList.add("bg-danger");
    }
    ResultBox.appendChild(questionBox);
  }
}

const submit_quiz = () => {
  const data = sendData();
  $.ajax({
    type: "POST",
    url: `${url}/calculate-result/`,
    data: data,
    success: (response) => showResults(response),
    error: (error) => console.log(error),
  });
}

// submit.addEventListener("click", (e) => {
//   e.preventDefault();
//   data = sendData();
//   $.ajax({
//     type: "POST",
//     url: `${url}/calculate-result/`,
//     data: data,
//     success: (response) => showResults(response),
//     error: (error) => console.log(error),
//   });
// });

submit.addEventListener("click", () => {
  clearInterval(timeInterval);
  submit_quiz();
});




