const collectionEl = document.getElementById("collection");
const questionEl = document.getElementById("question");
const askBtn = document.getElementById("ask");
const answerEl = document.getElementById("answer");

async function ask() {
  const question = questionEl.value.trim();
  if (!question) return;

  askBtn.disabled = true;
  askBtn.textContent = "Thinking...";
  answerEl.classList.remove("error");
  answerEl.classList.add("visible");
  answerEl.textContent = "";

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        collection: collectionEl.value,
      }),
    });

    if (!res.ok) {
      throw new Error(`Request failed (${res.status})`);
    }

    const data = await res.json();
    answerEl.textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
  } catch (err) {
    answerEl.classList.add("error");
    answerEl.textContent = `Error: ${err.message}`;
  } finally {
    askBtn.disabled = false;
    askBtn.textContent = "Ask";
  }
}

askBtn.addEventListener("click", ask);

questionEl.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
    ask();
  }
});
