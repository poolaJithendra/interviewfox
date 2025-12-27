document.getElementById("askBtn").addEventListener("click", () => {
  const question = document.getElementById("question").value.trim();
  const resume = document.getElementById("resume").value;
  const jd = document.getElementById("jd").value;
  const answerDiv = document.getElementById("answer");

  if (!question) {
    answerDiv.innerText = "Please paste a question.";
    return;
  }

  answerDiv.innerText = "";
  let buffer = "";

  const socket = new WebSocket("ws://localhost:8000/ws/answer");

  socket.onopen = () => {
    socket.send(
      JSON.stringify({
        question: question,
        resume: resume,
        job_description: jd,
      })
    );
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "start") {
      answerDiv.innerText = "Answer:\n\n";
      return;
    }

    if (data.type === "delta") {
      buffer += data.content;
      answerDiv.innerText = "Answer:\n\n" + buffer;
      return;
    }

    if (data.type === "done") {
      // final answer already displayed
      return;
    }

    if (data.type === "error") {
      answerDiv.innerText = "Error: " + (data.message || "Unknown error");
    }
  };

  socket.onerror = () => {
    answerDiv.innerText = "Connection error.";
  };
});
