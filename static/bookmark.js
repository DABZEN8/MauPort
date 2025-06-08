// bookmark.js
// Hanterar klick på favorit-/bokmärkesknappar för portfolioinlägg.
// Skickar POST till /toggle_favorite, uppdaterar ikon eller text på knappen.
// Tar även bort kort från sidan om det är på /favorites och inlägget tas bort.

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".bookmark-btn, .save-btn").forEach(button => {
    button.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const portfolioId = button.dataset.portfolioId;

      const res = await fetch("/toggle_favorite", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ portfolio_id: portfolioId })
      });

      const data = await res.json();

      if (data.success) {
        const icon = button.querySelector("i");
        const isFavoritesPage = window.location.pathname === "/favorites";

        if (icon) {
          icon.classList.toggle("fas", data.status === "added");
          icon.classList.toggle("far", data.status !== "added");
        } else {
          // textknapp fallback
          button.textContent = data.status === "added" ? "Inlägg sparad!" : "Borttagen";
          button.classList.toggle("active", data.status === "added");
        }

        if (isFavoritesPage && data.status === "removed") {
          const card = button.closest(".card, .portfolio-card");
          if (card) {
            card.classList.add("removed");
            setTimeout(() => card.remove(), 300);
          }
        }
      } else {
        alert(data.message || "Något gick fel.");
      }
    });
  });
});
