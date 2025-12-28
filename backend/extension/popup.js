// // // ===============================
// // // InterviewFox – Popup Logic
// // // ===============================

// // const API = "http://127.0.0.1:8000";

// // const resumeInput = document.getElementById("resumeFile");
// // const jdInput = document.getElementById("jdFile");
// // const createBtn = document.getElementById("createSessionBtn");
// // const icBtn = document.getElementById("icBtn");

// // const sessionInfo = document.getElementById("sessionInfo");
// // const capturedQ = document.getElementById("capturedQ");
// // const answerDiv = document.getElementById("answer");

// // let sessionId = null;

// // // -------------------------------
// // // Create session + upload files
// // // -------------------------------
// // createBtn.onclick = async () => {
// //   sessionInfo.innerText = "Creating session...";
// //   capturedQ.innerText = "";
// //   answerDiv.innerText = "";

// //   const sessionRes = await fetch(`${API}/session/create`, {
// //     method: "POST",
// //   });
// //   const sessionData = await sessionRes.json();
// //   sessionId = sessionData.session_id;

// //   const formData = new FormData();
// //   formData.append("session_id", sessionId);

// //   if (resumeInput.files[0]) {
// //     formData.append("resume_file", resumeInput.files[0]);
// //   }
// //   if (jdInput.files[0]) {
// //     formData.append("jd_file", jdInput.files[0]);
// //   }

// //   const uploadRes = await fetch(`${API}/session/upload`, {
// //     method: "POST",
// //     body: formData,
// //   });
// //   const uploadData = await uploadRes.json();

// //   sessionInfo.innerText =
// //     "Session created\n" +
// //     `Resume chars: ${uploadData.resume_chars}\n` +
// //     `JD chars: ${uploadData.jd_chars}`;
// // };

// // // -------------------------------
// // // IC Mode toggle
// // // -------------------------------
// // icBtn.onclick = () => {
// //   if (!sessionId) {
// //     alert("Create session first");
// //     return;
// //   }

// //   icBtn.innerText = "IC ON (Listening)";
// //   icBtn.disabled = true;

// //   window.open(
// //     `ic.html?session_id=${sessionId}`,
// //     "_blank",
// //     "width=600,height=400"
// //   );

// //   // poll for answer after IC closes
// //   setTimeout(() => {
// //     fetchAnswer();
// //     icBtn.innerText = "IC OFF (Muted)";
// //     icBtn.disabled = false;
// //   }, 4000);
// // };

// // // -------------------------------
// // // Fetch auto-generated answer
// // // -------------------------------
// // async function fetchAnswer() {
// //   const res = await fetch(
// //     `${API}/session/ic/answer?session_id=${sessionId}`,
// //     { method: "POST" }
// //   );

// //   const data = await res.json();

// //   if (data.question) {
// //     capturedQ.innerText = data.question;
// //   }

// //   if (data.answer) {
// //     answerDiv.innerText = data.answer;
// //   }
// // }


// // ===============================
// // InterviewFox – Popup Logic
// // ===============================

// const API = "http://127.0.0.1:8000";

// const resumeInput = document.getElementById("resumeFile");
// const jdInput = document.getElementById("jdFile");
// const createBtn = document.getElementById("createSessionBtn");
// const icBtn = document.getElementById("icBtn");

// const sessionInfo = document.getElementById("sessionInfo");
// const capturedQ = document.getElementById("capturedQ");
// const answerDiv = document.getElementById("answer");

// let sessionId = null;
// let answerPoller = null;

// // -------------------------------
// // Create session + upload files
// // -------------------------------
// createBtn.onclick = async () => {
//   sessionInfo.innerText = "Creating session...";
//   capturedQ.innerText = "";
//   answerDiv.innerText = "";

//   const sessionRes = await fetch(`${API}/session/create`, {
//     method: "POST",
//   });
//   const sessionData = await sessionRes.json();
//   sessionId = sessionData.session_id;

//   const formData = new FormData();
//   formData.append("session_id", sessionId);

//   if (resumeInput.files[0]) {
//     formData.append("resume_file", resumeInput.files[0]);
//   }
//   if (jdInput.files[0]) {
//     formData.append("jd_file", jdInput.files[0]);
//   }

//   const uploadRes = await fetch(`${API}/session/upload`, {
//     method: "POST",
//     body: formData,
//   });
//   const uploadData = await uploadRes.json();

//   sessionInfo.innerText =
//     "Session created\n" +
//     `Resume chars: ${uploadData.resume_chars}\n` +
//     `JD chars: ${uploadData.jd_chars}`;
// };

// // -------------------------------
// // IC Mode toggle (UNCHANGED FLOW)
// // -------------------------------
// icBtn.onclick = () => {
//   if (!sessionId) {
//     alert("Create session first");
//     return;
//   }

//   icBtn.innerText = "IC ON (Listening)";
//   icBtn.disabled = true;

//   // Open IC tab (mic lives here)
//   window.open(
//     `ic.html?session_id=${sessionId}`,
//     "_blank",
//     "width=600,height=400"
//   );

//   // Start polling for answer (robust)
//   startAnswerPolling();
// };

// // -------------------------------
// // Robust polling for answer
// // -------------------------------
// function startAnswerPolling() {
//   if (answerPoller) clearInterval(answerPoller);

//   answerPoller = setInterval(async () => {
//     const res = await fetch(
//       `${API}/session/ic/answer?session_id=${sessionId}`,
//       { method: "POST" }
//     );

//     const data = await res.json();

//     if (data.question) {
//       capturedQ.innerText = data.question;
//     }

//     if (data.answer) {
//       answerDiv.innerText = data.answer;

//       // Stop polling once answer is ready
//       clearInterval(answerPoller);
//       answerPoller = null;

//       icBtn.innerText = "IC OFF (Muted)";
//       icBtn.disabled = false;
//     }
//   }, 1000); // poll every 1 second
// }


document.getElementById("openApp").addEventListener("click", () => {
  chrome.tabs.create({
    url: chrome.runtime.getURL("app.html")
  });
});
