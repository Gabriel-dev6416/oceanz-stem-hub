(function () {
  var root = document.documentElement;

  // Light, Dark and System themes (NFR-23). "System" follows the device setting.
  var themeButtons = document.querySelectorAll("[data-theme-choice]");

  function savedTheme() {
    try {
      var theme = localStorage.getItem("theme");
      return theme === "light" || theme === "dark" ? theme : "system";
    } catch (e) {
      return root.dataset.theme || "system";
    }
  }

  function showTheme(choice) {
    themeButtons.forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.dataset.themeChoice === choice));
    });
  }

  themeButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      var choice = button.dataset.themeChoice;
      if (choice === "system") {
        delete root.dataset.theme;
      } else {
        root.dataset.theme = choice;
      }
      try {
        if (choice === "system") {
          localStorage.removeItem("theme");
        } else {
          localStorage.setItem("theme", choice);
        }
      } catch (e) {
        // Storage unavailable: the choice lasts for this page only.
      }
      showTheme(choice);
    });
  });
  showTheme(savedTheme());

  // Collapsed menu below 1200 px (FR-WEB-17).
  var menuToggle = document.querySelector("[data-menu-toggle]");
  var menu = document.getElementById("site-menu");
  if (menuToggle && menu) {
    menuToggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      menuToggle.setAttribute("aria-expanded", String(open));
      menuToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }
})();
