const task = document.getElementById("task");

const inputText =
    document.getElementById("inputText");

const inputLabel =
    document.getElementById("inputLabel");

const extraFields =
    document.getElementById("extraFields");

const submitBtn =
    document.getElementById("submitBtn");

const status =
    document.getElementById("status");

const resultCard =
    document.getElementById("resultCard");

const result =
    document.getElementById("result");

const copyBtn =
    document.getElementById("copyBtn");


// --------------------------------
// Render Additional Fields
// --------------------------------

function renderFields() {

    const selectedTask = task.value;

    extraFields.innerHTML = "";


    // EXPLAIN

    if (selectedTask === "explain") {

        extraFields.innerHTML = `
            <div class="field-row">

                <div class="form-group">

                    <label for="level">
                        Learner Level
                    </label>

                    <select id="level">

                        <option value="beginner">
                            Beginner
                        </option>

                        <option value="intermediate">
                            Intermediate
                        </option>

                        <option value="advanced">
                            Advanced
                        </option>

                    </select>

                </div>

            </div>
        `;

        inputLabel.textContent =
            "Topic";

        inputText.placeholder =
            "Example: Explain recursion in programming";

        submitBtn.textContent =
            "Explain Concept";

        return;
    }


    // LEARNING PATH

    if (selectedTask === "learn") {

        extraFields.innerHTML = `
            <div class="field-row">

                <div class="form-group">

                    <label for="level">
                        Learner Level
                    </label>

                    <select id="level">

                        <option value="beginner">
                            Beginner
                        </option>

                        <option value="intermediate">
                            Intermediate
                        </option>

                        <option value="advanced">
                            Advanced
                        </option>

                    </select>

                </div>


                <div class="form-group">

                    <label for="weeks">
                        Number of Weeks
                    </label>

                    <input
                        id="weeks"
                        type="number"
                        min="1"
                        max="52"
                        value="6"
                    >

                </div>

            </div>
        `;

        inputLabel.textContent =
            "Learning Topic";

        inputText.placeholder =
            "Example: Learn Python from zero";

        submitBtn.textContent =
            "Build Learning Path";

        return;
    }


    // QUIZ

    if (selectedTask === "quiz") {

        inputLabel.textContent =
            "Study Material";

        inputText.placeholder =
            "Paste your study material here...";

        submitBtn.textContent =
            "Generate Quiz";

        return;
    }


    // SUMMARY

    if (selectedTask === "summarize") {

        inputLabel.textContent =
            "Text to Summarize";

        inputText.placeholder =
            "Paste your study material here...";

        submitBtn.textContent =
            "Summarize";

        return;
    }


    // Q&A

    inputLabel.textContent =
        "Your Question";

    inputText.placeholder =
        "Example: What is the difference between RAM and ROM?";

    submitBtn.textContent =
        "Ask EduGenie";
}


task.addEventListener(
    "change",
    renderFields
);


renderFields();


// --------------------------------
// HTML Escape
// --------------------------------

function escapeHtml(text) {

    return String(text)
        .replace(
            /[&<>"']/g,
            function (character) {

                const map = {

                    "&": "&amp;",
                    "<": "&lt;",
                    ">": "&gt;",
                    '"': "&quot;",
                    "'": "&#039;"

                };

                return map[character];

            }
        );
}


// --------------------------------
// Run API Request
// --------------------------------

async function runTask() {

    const selectedTask =
        task.value;

    const text =
        inputText.value.trim();


    if (!text) {

        status.textContent =
            "Please enter some text first.";

        return;
    }


    let endpoint;

    let body;


    // Q&A

    if (selectedTask === "qa") {

        endpoint = "/qa";

        body = {
            question: text
        };

    }


    // EXPLAIN

    else if (selectedTask === "explain") {

        endpoint = "/explain";

        body = {

            topic: text,

            level:
                document
                    .getElementById("level")
                    .value

        };

    }


    // QUIZ

    else if (selectedTask === "quiz") {

        endpoint = "/quiz";

        body = {

            text: text,

            count: 3

        };

    }


    // SUMMARY

    else if (selectedTask === "summarize") {

        endpoint = "/summarize";

        body = {

            text: text

        };

    }


    // LEARNING PATH

    else if (selectedTask === "learn") {

        endpoint =
            "/learn/recommendations";

        body = {

            topic: text,

            level:
                document
                    .getElementById("level")
                    .value,

            weeks:
                Number(
                    document
                        .getElementById("weeks")
                        .value
                )

        };

    }


    submitBtn.disabled = true;

    status.textContent =
        "EduGenie is thinking...";

    resultCard.classList.add(
        "hidden"
    );

    result.innerHTML = "";


    try {

        const response =
            await fetch(
                endpoint,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(body)
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed"
            );

        }


        renderResult(
            selectedTask,
            data
        );


        resultCard.classList.remove(
            "hidden"
        );


        status.textContent =
            "Done.";


    } catch (error) {

        status.textContent =
            error.message;


    } finally {

        submitBtn.disabled =
            false;

    }
}


// --------------------------------
// Render Result
// --------------------------------

function renderResult(
    type,
    data
) {

    // Q&A

    if (type === "qa") {

        result.textContent =
            data.answer;

        return;
    }


    // EXPLAIN

    if (type === "explain") {

        result.textContent =
            data.explanation;

        return;
    }


    // SUMMARY

    if (type === "summarize") {

        result.textContent =
            data.summary;

        return;
    }


    // LEARNING PATH

    if (type === "learn") {

        result.textContent =
            data.recommendations;

        return;
    }


    // QUIZ

    if (type === "quiz") {

        result.innerHTML = "";


        data.quiz.forEach(
            (question, index) => {

                const box =
                    document.createElement(
                        "div"
                    );

                box.className =
                    "quiz-question";


                const heading =
                    document.createElement(
                        "h3"
                    );

                heading.innerHTML =
                    `${index + 1}. ${
                        escapeHtml(
                            question.question
                        )
                    }`;


                box.appendChild(
                    heading
                );


                question.options.forEach(
                    option => {

                        const button =
                            document.createElement(
                                "button"
                            );

                        button.className =
                            "option";


                        button.textContent =
                            option;


                        button.addEventListener(
                            "click",
                            () => {

                                const allOptions =
                                    box.querySelectorAll(
                                        ".option"
                                    );


                                allOptions.forEach(
                                    button =>
                                        button.disabled =
                                            true
                                );


                                if (
                                    option ===
                                    question.answer
                                ) {

                                    button.classList.add(
                                        "correct"
                                    );

                                } else {

                                    button.classList.add(
                                        "wrong"
                                    );


                                    allOptions.forEach(
                                        answerButton => {

                                            if (
                                                answerButton
                                                    .textContent ===
                                                question.answer
                                            ) {

                                                answerButton.classList.add(
                                                    "correct"
                                                );

                                            }

                                        }
                                    );

                                }


                                const explanation =
                                    document.createElement(
                                        "div"
                                    );


                                explanation.className =
                                    "explanation";


                                explanation.textContent =
                                    `Answer: ${
                                        question.answer
                                    }. ${
                                        question.explanation
                                    }`;


                                box.appendChild(
                                    explanation
                                );

                            }
                        );


                        box.appendChild(
                            button
                        );

                    }
                );


                result.appendChild(
                    box
                );

            }
        );

    }

}


// --------------------------------
// Submit
// --------------------------------

submitBtn.addEventListener(
    "click",
    runTask
);


// --------------------------------
// Copy Result
// --------------------------------

copyBtn.addEventListener(
    "click",
    async () => {

        try {

            await navigator.clipboard.writeText(
                result.innerText
            );

            copyBtn.textContent =
                "Copied";

            setTimeout(
                () => {

                    copyBtn.textContent =
                        "Copy";

                },
                1200
            );

        } catch {

            copyBtn.textContent =
                "Copy failed";

        }

    }
);