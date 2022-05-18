const url = window.location.href;
const quizForm = document.querySelector("#quiz-form");
const quizBox = document.querySelector(".quiz-box");
const submit = document.querySelector("#submit");
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
        <h4 class="font-medium text-capitalize"> <span class="me-3 text-primary">Question-${
          index + 1
        } :</span>${question}</h4>
        <div class="options mt-3 d-flex justify-content-between">
            ${answers
              .map((answer) => {
                return `
                <div class="form-check option d-flex align-items-center mt-3 px-5">
                    <input class="form-check-input answer" type="radio" name="${question}" id="${question}" value="${answer}">
                    <label class="form-check-label ms-3" style="font-size :medium; font-weight : 500" for="${question}">
                        ${answer}
                    </label>
                </div>`;
              })
              .join("")}
        </div>   
        <hr>
    </div>`;
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

function showResults(response) {}

submit.addEventListener("click", (e) => {
  e.preventDefault();
  data = sendData();
  $.ajax({
    type: "POST",
    url: `${url}/calculate-result`,
    data: data,
    success: (response) => showResults(response),
    error: (error) => console.log(error),
  });
});
