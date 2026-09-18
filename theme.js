(() => {
  const storageKey = "vellitas-theme";
  const root = document.documentElement;
  const media = window.matchMedia("(prefers-color-scheme: dark)");
  const allowedPreferences = new Set(["system", "light", "dark"]);

  const readPreference = () => {
    try {
      const saved = window.localStorage.getItem(storageKey);
      return allowedPreferences.has(saved) ? saved : "system";
    } catch {
      return "system";
    }
  };

  const resolvedTheme = (preference) =>
    preference === "system" ? (media.matches ? "dark" : "light") : preference;

  const applyPreference = (preference) => {
    const nextPreference = allowedPreferences.has(preference) ? preference : "system";
    const theme = resolvedTheme(nextPreference);
    root.dataset.themePreference = nextPreference;
    root.dataset.theme = theme;
    root.style.colorScheme = theme;

    const themeColor = document.querySelector('meta[name="theme-color"]');
    themeColor?.setAttribute("content", theme === "dark" ? "#020b14" : "#f4f7fa");

    window.dispatchEvent(
      new CustomEvent("vellitas:themechange", {
        detail: { preference: nextPreference, theme },
      }),
    );
  };

  const setPreference = (preference) => {
    try {
      if (preference === "system") window.localStorage.removeItem(storageKey);
      else window.localStorage.setItem(storageKey, preference);
    } catch {
      // The active page can still use the requested theme when storage is unavailable.
    }
    applyPreference(preference);
  };

  media.addEventListener?.("change", () => {
    if (readPreference() === "system") applyPreference("system");
  });

  window.vellitasTheme = { setPreference };
  applyPreference(readPreference());
})();
