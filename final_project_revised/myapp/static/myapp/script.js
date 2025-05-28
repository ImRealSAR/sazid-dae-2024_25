// Theme toggle script
document.addEventListener("DOMContentLoaded", function () {
  const body = document.body;
  const theme = localStorage.getItem("theme");
  if (theme === "light") {
    body.classList.add("light-mode");
  }

  const toggle = document.getElementById("theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      body.classList.toggle("light-mode");
      localStorage.setItem("theme", body.classList.contains("light-mode") ? "light" : "dark");
    });
  }
});
