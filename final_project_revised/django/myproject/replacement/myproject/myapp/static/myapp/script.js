document.getElementById("aiForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const prompt = document.getElementById("prompt").value;
    const output = document.getElementById("output");
    output.textContent = "Thinking...";
  
    const response = await fetch("/generate/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Basic " + btoa("admin:securepassword"),
      },
      body: JSON.stringify({ prompt }),
    });
  
    const data = await response.json();
    output.textContent = data.generated_text || data.error || "No response";
  });
  