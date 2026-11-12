// Applies a saved light/dark choice before the page paints, so there is no flash.
(function () {
  try {
    var theme = localStorage.getItem("theme");
    if (theme === "light" || theme === "dark") {
      document.documentElement.dataset.theme = theme;
    }
  } catch (e) {
    // Storage unavailable (private mode): fall back to the system setting.
  }
})();
