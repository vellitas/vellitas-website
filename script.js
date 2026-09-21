(() => {
  const header = document.querySelector("[data-header]");
  const menu = document.querySelector("[data-menu]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const navLinks = [...document.querySelectorAll(".site-nav a")];
  const revealItems = [...document.querySelectorAll(".reveal")];
  const sections = [...document.querySelectorAll("main section[id]")];
  const stageItems = [...document.querySelectorAll("[data-stage]")];
  const year = document.querySelector("[data-year]");
  const contactForm = document.querySelector("#contact-form");

  document.querySelectorAll("a[href]").forEach((link) => {
    let destination;
    try {
      destination = new URL(link.href, window.location.href);
    } catch {
      return;
    }

    if (!["http:", "https:"].includes(destination.protocol) || destination.origin === window.location.origin) return;
    link.target = "_blank";
    link.rel = "noopener noreferrer";

    if (!link.querySelector("[data-new-window-note]")) {
      const note = document.createElement("span");
      note.className = "sr-only";
      note.dataset.newWindowNote = "";
      note.textContent = " (opens in a new tab)";
      link.append(note);
    }
  });

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  const closeMenu = () => {
    if (!menu || !menuToggle) return;
    menu.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Open navigation");
    document.body.classList.remove("menu-open");
  };

  menuToggle?.addEventListener("click", () => {
    const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
    menu?.classList.toggle("is-open", !isOpen);
    menuToggle.setAttribute("aria-expanded", String(!isOpen));
    menuToggle.setAttribute("aria-label", isOpen ? "Open navigation" : "Close navigation");
    document.body.classList.toggle("menu-open", !isOpen);
  });

  navLinks.forEach((link) => link.addEventListener("click", closeMenu));

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });

  const onScroll = () => {
    header?.classList.toggle("is-scrolled", window.scrollY > 24);
  };

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.14, rootMargin: "0px 0px -6%" },
    );

    revealItems.forEach((item) => revealObserver.observe(item));

    const sectionObserver = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

        if (!visible) return;
        navLinks.forEach((link) => {
          link.classList.toggle("is-current", link.getAttribute("href") === `#${visible.target.id}`);
        });
      },
      { threshold: [0.2, 0.45, 0.7], rootMargin: "-18% 0px -50%" },
    );

    sections.forEach((section) => sectionObserver.observe(section));
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }

  stageItems.forEach((item) => {
    const button = item.querySelector("button");
    button?.addEventListener("click", () => {
      stageItems.forEach((stage) => {
        const active = stage === item;
        stage.classList.toggle("is-active", active);
        stage.querySelector("button")?.setAttribute("aria-pressed", String(active));
      });
    });
  });

  if (contactForm instanceof HTMLFormElement) {
    const startedAt = contactForm.elements.namedItem("startedAt");
    const submitButton = contactForm.querySelector("button[type='submit']");
    const status = contactForm.querySelector("[role='status']");

    const resetStartedAt = () => {
      if (startedAt instanceof HTMLInputElement) startedAt.value = String(Date.now());
    };

    resetStartedAt();

    contactForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!contactForm.reportValidity()) return;

      const formData = new FormData(contactForm);
      const payload = {
        name: String(formData.get("name") || ""),
        email: String(formData.get("email") || ""),
        organization: String(formData.get("organization") || ""),
        role: String(formData.get("role") || ""),
        message: String(formData.get("message") || ""),
        consent: formData.get("consent") === "on",
        website: String(formData.get("website") || ""),
        startedAt: Number(formData.get("startedAt") || 0),
      };

      if (payload.message.trim().length < 20) {
        const messageField = contactForm.elements.namedItem("message");
        if (messageField instanceof HTMLTextAreaElement) {
          messageField.setCustomValidity("Please tell us a little more about what you want to assess.");
          messageField.reportValidity();
          messageField.addEventListener("input", () => messageField.setCustomValidity(""), { once: true });
        }
        return;
      }

      contactForm.setAttribute("aria-busy", "true");
      if (submitButton instanceof HTMLButtonElement) submitButton.disabled = true;
      if (status) {
        status.className = "contact-form__status";
        status.textContent = "Sending your request…";
      }

      try {
        const response = await fetch(contactForm.action, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(payload),
          credentials: "same-origin",
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(result.error || "We could not send your request.");
        contactForm.reset();
        resetStartedAt();
        if (status) {
          status.className = "contact-form__status is-success";
          status.textContent = "Thank you. Your request was received, and Vellitas will follow up.";
        }
      } catch (error) {
        if (status) {
          status.className = "contact-form__status is-error";
          status.textContent = error instanceof Error
            ? error.message
            : "We could not send your request. Please try again shortly.";
        }
      } finally {
        contactForm.removeAttribute("aria-busy");
        if (submitButton instanceof HTMLButtonElement) submitButton.disabled = false;
      }
    });
  }
})();
