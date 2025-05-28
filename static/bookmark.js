document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".save-btn").forEach(button => {
    button.addEventListener("click", async (e) => {
      e.preventDefault();
      const portfolioId = button.dataset.portfolioId;

      try {
        const res = await fetch("/save_favorite", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ portfolio_id: portfolioId })
        });

        const data = await res.json();
        if (data.success) {
          button.textContent = "Sparad!";
          button.disabled = true;
        } else {
          alert(data.message || "Något gick fel.");
        }

      } catch (err) {
        console.error("Fel vid spara-försök:", err);
        alert("Ett tekniskt fel inträffade.");
      }
    });
  });
});
