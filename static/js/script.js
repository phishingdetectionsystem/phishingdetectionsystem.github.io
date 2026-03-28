
const API_URL = "/api";

// =====================
// GET ELEMENTS
// =====================
const urlForm = document.getElementById("urlForm");
const urlInput = document.getElementById("urlInput");
const submitButton = document.getElementById("submitButton");
const resultsDiv = document.getElementById("results");
const loadingDiv = document.getElementById("loading");
const formContainer = document.querySelector(".form-container");
const featuresSection = document.getElementById("featuresSection");

// =====================
// URL HELPERS
// =====================
function normalizeURL(url) {
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        url = "https://" + url;
    }
    return url;
}

function isValidURL(string) {
    try {
        new URL(string);
        return true;
    } catch {
        return false;
    }
}

// =====================
// UI HELPERS
// =====================
function showLoading() {
    loadingDiv.style.display = "block";
    resultsDiv.style.display = "none";
    submitButton.disabled = true;
    submitButton.textContent = "Checking...";
}

function hideLoading() {
    loadingDiv.style.display = "none";
    submitButton.disabled = false;
    submitButton.textContent = "Check URL";
}

function showError(message) {
    resultsDiv.innerHTML = `
        <div class="error-card">
            <h3>❌ Error</h3>
            <p>${message}</p>
        </div>
    `;
    resultsDiv.style.display = "block";
}

// =====================
// DISPLAY RESULTS
// =====================
function displayResults(result) {
    // Hide home sections
    formContainer.style.display = "none";
    featuresSection.style.display = "none";

    const isPhishing = result.is_phishing;
    const statusColor = isPhishing ? "#dc3545" : "#28a745";
    const statusText = isPhishing ? "⚠️ PHISHING DETECTED" : "✅ SAFE";

    const phishingPercent = result.confidence;
    const safePercent = 100 - phishingPercent;

    resultsDiv.innerHTML = `
        <!-- 🔙 BACK BUTTON -->
        <button id="backButton" class="back-btn">⬅ Back</button>

        <div class="result-card" style="padding:25px; font-size:18px;">

            <h2 style="
                color:${statusColor};
                text-align:center;
                font-size:36px;
                margin-bottom:30px;
            ">
                ${statusText}
            </h2>

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:30px;
                flex-wrap:wrap;
            ">

                <div style="
                    flex:1;
                    min-width:300px;
                    font-size:22px;
                    line-height:1.6;
                ">
                    <p><strong>URL:</strong> ${result.url}</p>
                    <p><strong>Confidence:</strong> ${result.confidence.toFixed(2)}%</p>
                    <p><strong>Risk Level:</strong> ${result.risk_level}</p>
                    <p><strong>Recommendation:</strong> ${result.recommendation}</p>
                </div>

                <div style="width:320px;">
                    <canvas id="riskChart"></canvas>
                </div>

            </div>
        </div>
    `;

    resultsDiv.style.display = "block";

    // PIE CHART
    const ctx = document.getElementById("riskChart");
    new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Safe", "Phishing Risk"],
            datasets: [{
                data: [safePercent, phishingPercent],
                backgroundColor: ["#28a745", "#dc3545"]
            }]
        },
        options: {
    plugins: {
        legend: {
            position: "bottom",
            labels: {
                font: { size: 16 }
            },
            // ✅ disable click (no button behaviour)
            onClick: () => {}
        }
    },
    // ✅ remove pointer cursor
    onHover: (e) => {
        e.native.target.style.cursor = "default";
    }
}
    });

    // BACK BUTTON LOGIC
    document.getElementById("backButton").addEventListener("click", () => {
        resultsDiv.style.display = "none";
        formContainer.style.display = "block";
        featuresSection.style.display = "block";
        urlInput.value = "";
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}

// =====================
// API CALL
// =====================
async function checkURL(url) {
    try {
        showLoading();

        const response = await fetch(`${API_URL}/check-url`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        if (!response.ok) {
            throw new Error("Server Error");
        }

        const data = await response.json();
        hideLoading();
        displayResults(data);

    } catch (error) {
        hideLoading();
        showError(error.message);
    }
}

// =====================
// FORM SUBMIT
// =====================
urlForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    let url = urlInput.value.trim();
    if (!url) {
        showError("Please enter a URL");
        return;
    }

    url = normalizeURL(url);

    if (!isValidURL(url)) {
        showError("Invalid URL format");
        return;
    }

    await checkURL(url);
});