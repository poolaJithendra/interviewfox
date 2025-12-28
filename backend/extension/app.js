// ===============================
// InterviewFox – App Logic
// ===============================
const resumeInput = document.getElementById("resumeFile");
const jdInput = document.getElementById("jdFile");
const uploadBtn = document.getElementById("uploadBtn");

let sessionId = null;

const startBtn = document.getElementById("startMic");
const stopBtn = document.getElementById("stopMic");
const questionBox = document.getElementById("capturedQ");
const answerBox = document.getElementById("answer");

let recognition;
let finalTranscript = "";

// -------------------------------
// SAFETY CHECK
// -------------------------------
if (!startBtn || !stopBtn) {
  alert("Button IDs not found. Check app.html");
}

// -------------------------------
// START MIC
// -------------------------------
startBtn.onclick = () => {
  if (!("webkitSpeechRecognition" in window)) {
    alert("Speech recognition not supported in this browser");
    return;
  }

  recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.continuous = true;
  recognition.interimResults = true;

  finalTranscript = "";
  questionBox.value = "";
  answerBox.value = "";

  recognition.onresult = (event) => {
    let interim = "";

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript += transcript + " ";
      } else {
        interim += transcript;
      }
    }

    questionBox.value = finalTranscript + interim;
  };

  recognition.onerror = (e) => {
    console.error("Mic error:", e);
    alert("Microphone error");
  };

  recognition.start();

  startBtn.disabled = true;
  stopBtn.disabled = false;
};

// -------------------------------
// STOP MIC + GENERATE ANSWER
// -------------------------------
stopBtn.onclick = async () => {
  if (recognition) recognition.stop();

  startBtn.disabled = false;
  stopBtn.disabled = true;

  const question = finalTranscript.trim();
  if (!question) return;

  // 🔥 CALL BACKEND
  const res = await fetch("http://127.0.0.1:8000/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  const data = await res.json();
  answerBox.value = data.answer || "";
};
let generateTimer = null;

function autoGenerate(question) {
  clearTimeout(generateTimer);

  generateTimer = setTimeout(async () => {
    const res = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    answerBox.value = data.answer || "";
  }, 1500); // silence window
}
uploadBtn.onclick = async () => {
  if (!resumeInput.files.length && !jdInput.files.length) {
    alert("Upload resume or JD");
    return;
  }

  // create session
  const s = await fetch("http://127.0.0.1:8000/session/create", {
    method: "POST"
  });
  const sd = await s.json();
  sessionId = sd.session_id;

  const form = new FormData();
  form.append("session_id", sessionId);

  if (resumeInput.files[0]) {
    form.append("resume_file", resumeInput.files[0]);
  }
  if (jdInput.files[0]) {
    form.append("jd_file", jdInput.files[0]);
  }

  await fetch("http://127.0.0.1:8000/session/upload", {
    method: "POST",
    body: form
  });

  alert("Resume & JD uploaded");
};
