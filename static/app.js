const passwordInput = document.getElementById("passwordInput");
const toggleEye = document.getElementById("toggleEye");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultsWrapper = document.getElementById("resultsWrapper");
const downloadBtn = document.getElementById("downloadBtn");

let lastPassword = "";

toggleEye.addEventListener("click", () => {
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    toggleEye.textContent = "🙈";
  } else {
    passwordInput.type = "password";
    toggleEye.textContent = "👁";
  }
});

passwordInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    analyzeBtn.click();
  }
});

function strengthColor(strength) {
  switch (strength) {
    case "Very Weak":
      return "#ff5c5c";
    case "Weak":
      return "#ff8a3d";
    case "Moderate":
      return "#ffb100";
    case "Strong":
      return "#4da6ff";
    case "Very Strong":
      return "#00e5a0";
    default:
      return "#8b949e";
  }
}

function checkRow(label, passed) {
  return `
    <div class="check-item">
      <span>${label}</span>
      <span class="${passed ? "check-pass" : "check-fail"}">${passed ? "✔" : "✘"}</span>
    </div>
  `;
}

analyzeBtn.addEventListener("click", async () => {
  const password = passwordInput.value;

  if (!password) {
    alert("Please enter a password first.");
    return;
  }

  lastPassword = password;
  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });

    const data = await res.json();

    if (data.error) {
      alert(data.error);
      return;
    }

    renderResults(data);
    resultsWrapper.style.display = "block";
    resultsWrapper.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    alert("Something went wrong while analyzing. Please try again.");
    console.error(err);
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze";
  }
});

function renderResults(data) {
  const color = strengthColor(data.strength);

  document.getElementById("checkGrid").innerHTML = `
    ${checkRow("Length (min 12)", data.policy.length)}
    ${checkRow("Uppercase", data.policy.uppercase)}
    ${checkRow("Lowercase", data.policy.lowercase)}
    ${checkRow("Numbers", data.policy.numbers)}
    ${checkRow("Special Character", data.policy.special)}
  `;

  document.getElementById("infoGrid").innerHTML = `
    <div class="info-box">
      <div class="info-label">Entropy</div>
      <div class="info-value">${data.entropy} bits</div>
    </div>
    <div class="info-box">
      <div class="info-label">Entropy Rating</div>
      <div class="info-value">${data.entropy_label}</div>
    </div>
    <div class="info-box">
      <div class="info-label">Dictionary Attack</div>
      <div class="info-value" style="color:${data.dictionary_attack.vulnerable ? "#ff5c5c" : "#00e5a0"}">
        ${data.dictionary_attack.vulnerable ? "Vulnerable" : "Safe"}
      </div>
    </div>
    <div class="info-box">
      <div class="info-label">Common Password</div>
      <div class="info-value" style="color:${data.common_password.is_common ? "#ff5c5c" : "#00e5a0"}">
        ${data.common_password.is_common ? "Yes" : "No"}
      </div>
    </div>
    <div class="info-box">
      <div class="info-label">Keyboard Pattern</div>
      <div class="info-value" style="color:${data.keyboard_pattern.detected ? "#ff5c5c" : "#00e5a0"}">
        ${data.keyboard_pattern.detected ? "Detected" : "None"}
      </div>
    </div>
    <div class="info-box">
      <div class="info-label">Repeated / Sequential</div>
      <div class="info-value" style="color:${(data.repeated_chars.detected || data.sequential_chars.detected) ? "#ff5c5c" : "#00e5a0"}">
        ${(data.repeated_chars.detected || data.sequential_chars.detected) ? "Detected" : "None"}
      </div>
    </div>
  `;

  document.getElementById("meterFill").style.width = data.score + "%";
  document.getElementById("meterFill").style.background = color;
  document.getElementById("meterLabel").textContent = data.strength;
  document.getElementById("meterLabel").style.color = color;

  document.getElementById("scoreNumber").textContent = data.score;
  document.getElementById("scoreNumber").style.color = color;

  document.getElementById("strengthBadge").textContent = data.strength;
  document.getElementById("strengthBadge").style.background = color + "22";
  document.getElementById("strengthBadge").style.color = color;
  document.getElementById("strengthBadge").style.border = "1px solid " + color;

  document.getElementById("crackTime").textContent = data.crack_time_estimate;

  const suggList = document.getElementById("suggestionsList");
  suggList.innerHTML = "";
  data.suggestions.forEach((s) => {
    const li = document.createElement("li");
    li.textContent = s;
    suggList.appendChild(li);
  });
}

downloadBtn.addEventListener("click", async () => {
  if (!lastPassword) {
    alert("Please analyze a password first.");
    return;
  }

  downloadBtn.disabled = true;
  downloadBtn.textContent = "Generating PDF...";

  try {
    const res = await fetch("/report/pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: lastPassword }),
    });

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "SecurePass_Report.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    alert("Could not generate report. Please try again.");
    console.error(err);
  } finally {
    downloadBtn.disabled = false;
    downloadBtn.textContent = "Download PDF Report";
  }
});
