document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".save-btn").forEach(button => {
    button.addEventListener("click", async (e) => {
      e.preventDefault();
      const portfolioId = button.dataset.portfolioId;

      const res = await fetch("/toggle_favorite", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ portfolio_id: portfolioId })
      });

      const data = await res.json();

      if (data.success) {
        const isFavoritesPage = window.location.pathname === "/favorites";

        if (data.status === "added") {
          button.textContent = "Inlägg sparad!";
          button.classList.add("active");
        } else {
          if (isFavoritesPage) {
            const card = button.closest(".portfolio-card");
            if (card) card.remove();
          } else {
            button.textContent = "Spara inlägg";
            button.classList.remove("active");
          }
        }
      } else {
        alert(data.message || "Något gick fel.");
      }
    });
  });
});
