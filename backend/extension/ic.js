// ===============================
// InterviewFox – IC MODE
// ===============================

const urlParams = new URLSearchParams(window.location.search);
const sessionId = urlParams.get("session_id");

const transcriptDiv = document.getElementById("transcript");

if (!sessionId) {
  document.body.innerText = "Session ID missing";
  throw new Error("Session ID missing");
}

// -------------------------------
// Speech Recognition Setup
// -------------------------------
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
  alert("Speech Recognition not supported in this browser");
  throw new Error("SpeechRecognition unsupported");
}

const recognition = new SpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = "en-US";

let finalTranscript = "";

// -------------------------------
// Start IC mode on backend
// -------------------------------
fetch(
  `http://127.0.0.1:8000/session/ic/start?session_id=${sessionId}`,
  { method: "POST" }
);

// -------------------------------
// Speech events
// -------------------------------
recognition.onresult = async (event) => {
  let interim = "";

  for (let i = event.resultIndex; i < event.results.length; i++) {
    const text = event.results[i][0].transcript;

    if (event.results[i].isFinal) {
      finalTranscript += text + " ";

      await fetch(
        `http://127.0.0.1:8000/session/ic/append?session_id=${sessionId}&text=${encodeURIComponent(
          text
        )}`,
        { method: "POST" }
      );
    } else {
      interim += text;
    }
  }

  transcriptDiv.innerText = finalTranscript + "\n" + interim;
};

recognition.onerror = (e) => {
  console.error("Speech error:", e);
};

recognition.start();

// -------------------------------
// STOP button
// -------------------------------
document.getElementById("stopBtn").onclick = async () => {
  recognition.stop();

  // finalize transcript
  await fetch(
    `http://127.0.0.1:8000/session/ic/stop?session_id=${sessionId}`,
    { method: "POST" }
  );

  // auto-generate answer
  await fetch(
    `http://127.0.0.1:8000/session/ic/answer?session_id=${sessionId}`,
    { method: "POST" }
  );

  window.close();
};
