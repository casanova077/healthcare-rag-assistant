const questionInput = document.getElementById("question");
const answerBox = document.getElementById("answer");
const answerSection = document.getElementById("answerSection");
const loading = document.getElementById("loading");
const askButton = document.getElementById("askButton");


function setQuestion(question) {

    questionInput.value = question;

    questionInput.focus();

}


async function askQuestion() {

    const question = questionInput.value.trim();

    if (!question) {

        questionInput.focus();

        return;

    }

    loading.style.display = "flex";

    answerSection.style.display = "none";

    askButton.disabled = true;

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });


        if (!response.ok) {

            throw new Error("Server error");

        }


        const data = await response.json();

        answerBox.innerText = data.answer;

        answerSection.style.display = "block";

        answerSection.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    }

    catch (error) {

        answerBox.innerText =
            "Unable to retrieve the information. Please try again.";

        answerSection.style.display = "block";

        console.error(error);

    }

    finally {

        loading.style.display = "none";

        askButton.disabled = false;

    }

}


/* Ctrl + Enter to ask */

questionInput.addEventListener("keydown", function(event) {

    if (event.ctrlKey && event.key === "Enter") {

        askQuestion();

    }

});