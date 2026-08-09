document.addEventListener("DOMContentLoaded", () => {
  const currentPath = window.location.pathname;
  document.querySelectorAll(".sidebar-link[href]").forEach((link) => {
    const path = new URL(link.href).pathname;
    if ((path !== "/" && currentPath.startsWith(path)) || (path === "/" && currentPath === "/")) link.classList.add("active");
  });
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => form.querySelectorAll("button[type='submit']").forEach((button) => {
      button.disabled = true;
      button.setAttribute("aria-busy", "true");
    }));
  });
  document.querySelectorAll("[data-password-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const input = button.closest(".login-password-wrap")?.querySelector("input");
      if (!input) return;
      const showing = input.type === "text";
      input.type = showing ? "password" : "text";
      button.setAttribute("aria-label", showing ? "Mostrar senha" : "Ocultar senha");
      button.setAttribute("title", showing ? "Mostrar senha" : "Ocultar senha");
      const icon = button.querySelector("i");
      icon?.classList.toggle("bi-eye", showing);
      icon?.classList.toggle("bi-eye-slash", !showing);
    });
  });
});

document.body.addEventListener("htmx:configRequest", (event) => {
  const token = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
  if (token) event.detail.headers["X-CSRFToken"] = token;
});
