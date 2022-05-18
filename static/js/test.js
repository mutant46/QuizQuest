const url = window.location.href;
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
  questions_data.forEach((el) => {
    for (const [question, answers] of Object.entries(el))
      [generate_html(question, answers)];
  });
}

function generate_html(question, answers) {
  quizBox.innerHTML += `
    <div class="question mb-5">
        <h4>${question}</h4>
        <hr>
        <div class="options mt-3 d-flex w-50 justify-content-between">
            ${answers
              .map((answer) => {
                return `
                <div class="form-check option d-flex align-items-center">
                    <input class="form-check-input answer" type="radio" name="${question}" id="${question}" value="${answer}">
                    <label class="form-check-label ms-3" for="${question}">
                        ${answer}
                    </label>
                </div>`;
              })
              .join("")}
        </div>   
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


function redirect_to_next_url(response) {
  const url = response.next_url;
  window.location.replace(url);
}


submit.addEventListener("click", (e) => {
  e.preventDefault();
  data = sendData();
  $.ajax({
    type: "POST",
    url: `${url}/calculate-result`,
    data: data,
    success: (response) => console.log(response),
    error: (error) => console.log(error),
  })
})

