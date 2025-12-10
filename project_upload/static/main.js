// static/main.js
// Handles file uploads and API calls for Agentic Code Reviewer (LLM-only version)

document.addEventListener("DOMContentLoaded", () => {
  const reviewBtn = document.getElementById("reviewBtn");
  const reviewCombineBtn = document.getElementById("reviewCombineBtn");
  const reviewZipBtn = document.getElementById("reviewZipBtn");
  const resultsDiv = document.getElementById("results");

  // Helper to show loading animation
  const setLoading = (loading) => {
    if (loading) {
      resultsDiv.innerHTML = `<div class="loading">⏳ Analyzing your code... Please wait.</div>`;
    }
  };

  // Function to render results nicely
  const showResults = (data) => {
    let html = `<div class="result-card"><h3>✅ Analysis complete</h3>`;
    html += `<p><strong>Report ID:</strong> ${data.report_id}</p>`;
    html += `<p><strong>Files processed:</strong> ${data.files.join(", ")}</p>`;
    html += `<div class="button-row">
                <a class="btn-primary" href="/api/download-latest" target="_blank">📥 Download Latest PDF</a>
             </div>`;
    html += `<h4>🧠 AI Review Preview:</h4>`;
    html += `<div class="ai-review">`;

    if (data.previews) {
      for (const [fname, content] of Object.entries(data.previews)) {
        html += `<div class="file-review">
                   <h5>📄 ${fname}</h5>
                   <pre>${content.llm_summary || "No summary"}</pre>
                 </div>`;
      }
    } else if (data.llm_summary) {
      html += `<pre>${data.llm_summary}</pre>`;
    }
    html += `</div></div>`;
    resultsDiv.innerHTML = html;
  };

  // Common upload handler
  const uploadFiles = async (endpoint, filesFieldName, files) => {
    const formData = new FormData();
    for (const file of files) {
      formData.append(filesFieldName, file);
    }

    setLoading(true);

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errText = await res.text();
        resultsDiv.innerHTML = `<div class="error">❌ Error: ${errText}</div>`;
        return;
      }

      const data = await res.json();
      showResults(data);
    } catch (err) {
      resultsDiv.innerHTML = `<div class="error">🚨 ${err.message}</div>`;
    }
  };

  // Button actions
  reviewBtn.addEventListener("click", () => {
    const input = document.getElementById("fileInput");
    const files = input.files;
    if (!files.length) {
      alert("Please select a file first.");
      return;
    }
    uploadFiles("/api/review", "files", files);
  });

  reviewCombineBtn.addEventListener("click", () => {
    const input = document.getElementById("fileInput");
    const files = input.files;
    if (!files.length) {
      alert("Please select files first.");
      return;
    }
    uploadFiles("/api/review-multi", "files", files);
  });

  reviewZipBtn.addEventListener("click", () => {
    const input = document.getElementById("zipInput");
    const files = input.files;
    if (!files.length) {
      alert("Please choose a ZIP file.");
      return;
    }
    uploadFiles("/api/review-zip", "zip_file", files);
  });
});
