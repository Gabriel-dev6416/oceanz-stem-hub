// Applies a saved light/dark choice before the page paints, so there is no flash.
(function () {
  // Lets CSS collapse the mobile menu only when the script that opens it can run.
  document.documentElement.classList.add("js");
  try {
    var theme = localStorage.getItem("theme");
    if (theme === "light" || theme === "dark") {
      document.documentElement.dataset.theme = theme;
    }
  } catch (e) {
    // Storage unavailable (private mode): fall back to the system setting.
  }
})();
