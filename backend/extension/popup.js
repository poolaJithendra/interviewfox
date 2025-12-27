const API_BASE = "http://localhost:8000";
const WS_URL = "ws://localhost:8000/ws/answer";

let sessionId = null;
let icOn = false;

const sessionInfo = document.getElementById("sessionInfo");
const capturedQ = document.getElementById("capturedQ");
const answerDiv = document.getElementById("answer");
const icBtn = document.getElementById("icBtn");

/* -------------------------
   Session + Upload
-------------------------- */
async function createSessionAndUpload() {
  sessionInfo.innerText = "Creating session...";
  answerDiv.innerText = "";
  capturedQ.innerText = "";

  // Create session
  const res = await fetch(`${API_BASE}/session/create`, { method: "POST" });
  const data = await res.json();
  sessionId = data.session_id;

  // Upload resume & JD
  const resumeFile = document.getElementById("resumeFile").files[0];
  const jdFile = document.getElementById("jdFile").files[0];

  const form = new FormData();
  form.append("session_id", sessionId);
  if (resumeFile) form.append("resume_file", resumeFile);
  if (jdFile) form.append("jd_file", jdFile);

  const uploadRes = await fetch(`${API_BASE}/session/upload`, {
    method: "POST",
    body: form,
  });

  const uploadData = await uploadRes.json();

  sessionInfo.innerText =
    `Session: ${uploadData.session_id}\n` +
    `Resume chars: ${uploadData.resume_chars}, JD chars: ${uploadData.jd_chars}`;
}

/* -------------------------
   IC MODE
-------------------------- */
async function icStart() {
  await fetch(`${API_BASE}/session/ic/start?session_id=${sessionId}`, {
    method: "POST",
  });

  capturedQ.innerText = "";
  answerDiv.innerText = "IC ON… listening for interviewer question.";
}

async function icStopAndAnswer() {
  answerDiv.innerText = "Processing question…";

  const res = await fetch(
    `${API_BASE}/session/ic/stop?session_id=${sessionId}`,
    { method: "POST" }
  );
  const data = await res.json();

  const question = (data.question || "").trim();
  capturedQ.innerText = question || "(No speech captured)";

  if (!question) {
    answerDiv.innerText = "No question detected. Try IC ON again.";
    return;
  }

  // Open WebSocket for streaming answer
  let buffer = "";
  const socket = new WebSocket(WS_URL);

  socket.onopen = () => {
    socket.send(
      JSON.stringify({
        question: question,
        resume: "",           // handled via session on backend (next refinement)
        job_description: ""
      })
    );
  };

  socket.onmessage = (event) => {
    const msg = JSON.parse(event.data);

    if (msg.type === "start") {
      answerDiv.innerText = "Answer:\n\n";
      return;
    }

    if (msg.type === "delta") {
      buffer += msg.content;
      answerDiv.innerText = "Answer:\n\n" + buffer;
      return;
    }

    if (msg.type === "error") {
      answerDiv.innerText = "Error: " + msg.message;
    }
  };

  socket.onerror = () => {
    answerDiv.innerText = "WebSocket connection error.";
  };
}

/* -------------------------
   Button Handlers
-------------------------- */
document
  .getElementById("createSessionBtn")
  .addEventListener("click", async () => {
    try {
      await createSessionAndUpload();
    } catch (e) {
      sessionInfo.innerText = "Error: " + e.message;
    }
  });

icBtn.addEventListener("click", async () => {
  if (!sessionId) {
    answerDiv.innerText = "Please create session first.";
    return;
  }

  try {
    if (!icOn) {
      icOn = true;
      icBtn.innerText = "IC ON (Listening)";
      await icStart();
    } else {
      icOn = false;
      icBtn.innerText = "IC OFF (Muted)";
      await icStopAndAnswer();
    }
  } catch (e) {
    answerDiv.innerText = "Error: " + e.message;
  }
});
