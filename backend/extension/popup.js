document.getElementById("askBtn").addEventListener("click", () => {
  const question = document.getElementById("question").value;
  const resume = document.getElementById("resume").value;
  const jd = document.getElementById("jd").value;
  const answerDiv = document.getElementById("answer");

  answerDiv.innerText = "Thinking...";

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
    if (data.type === "answer") {
      answerDiv.innerText = data.content;
    }
  };

  socket.onerror = () => {
    answerDiv.innerText = "Connection error.";
  };
});
