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

  // Dismissible notice bar (FR-WEB-19). A changed notice gets a new id and shows again.
  var notice = document.querySelector("[data-notice-id]");
  if (notice) {
    var dismissed = null;
    try {
      dismissed = localStorage.getItem("noticeDismissed");
    } catch (e) {
      // Storage unavailable: the notice shows on every page.
    }
    if (dismissed !== notice.dataset.noticeId) {
      notice.classList.add("is-visible");
    }
    notice.querySelector("[data-notice-close]").addEventListener("click", function () {
      notice.classList.remove("is-visible");
      try {
        localStorage.setItem("noticeDismissed", notice.dataset.noticeId);
      } catch (e) {
        // Storage unavailable: dismissed for this page only.
      }
    });
  }

  // Programmes dropdown (FR-WEB-17).
  document.querySelectorAll("[data-sub-toggle]").forEach(function (button) {
    var item = button.closest(".has-sub");
    button.addEventListener("click", function () {
      var open = item.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", function (event) {
      if (!item.contains(event.target)) {
        item.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
      }
    });
    item.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        item.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
        button.focus();
      }
    });
  });

  // Copy buttons for bank details (FR-PAY-05).
  if (navigator.clipboard) {
    document.querySelectorAll("[data-copy]").forEach(function (button) {
      button.hidden = false;
      button.addEventListener("click", function () {
        function show(label) {
          button.textContent = label;
          setTimeout(function () {
            button.textContent = "Copy";
          }, 2500);
        }
        navigator.clipboard.writeText(button.dataset.copy).then(
          function () {
            show("Copied");
          },
          function () {
            // Clipboard refused: select the text so it can be copied by hand.
            var range = document.createRange();
            range.selectNodeContents(button.previousElementSibling);
            var selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
            show("Selected");
          }
        );
      });
    });
  }

  // Cookie notice (FR-WEB-12): shown until the visitor closes it.
  var cookieNotice = document.querySelector("[data-cookie-notice]");
  if (cookieNotice) {
    var seen = null;
    try {
      seen = localStorage.getItem("cookieNotice");
    } catch (e) {
      // Storage unavailable: the notice shows on each page.
    }
    if (!seen) {
      cookieNotice.classList.add("is-visible");
    }
    cookieNotice.querySelector("[data-cookie-ok]").addEventListener("click", function () {
      cookieNotice.classList.remove("is-visible");
      try {
        localStorage.setItem("cookieNotice", "seen");
      } catch (e) {
        // Storage unavailable: closed for this page only.
      }
    });
  }

  // Google Maps loads only when the visitor asks for it, because it sets its own cookies.
  document.querySelectorAll("[data-map-src]").forEach(function (frame) {
    var button = frame.querySelector("[data-map-load]");
    button.hidden = false;
    button.addEventListener("click", function () {
      var iframe = document.createElement("iframe");
      iframe.src = frame.dataset.mapSrc;
      iframe.title = "Map showing the OCEANZ STEM HUB location";
      iframe.referrerPolicy = "no-referrer-when-downgrade";
      frame.classList.remove("map-placeholder");
      frame.classList.add("skeleton");
      frame.replaceChildren(iframe);
    });
  });

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
