let fileInput = document.getElementById("fileInput");
let previewContainer = document.getElementById("fileList");
let selectedFiles = [];

fileInput.addEventListener("change", function (event) {
  const newFiles = Array.from(event.target.files);

  // Lägg till nya filer utan att ersätta gamla
  newFiles.forEach((newFile) => {
    // Förhindra dubbletter baserat på filnamn och storlek
    const exists = selectedFiles.some(f => f.name === newFile.name && f.size === newFile.size);
    if (!exists) {
      selectedFiles.push(newFile);
    }
  });

  renderPreviews();

  // Skapa ett nytt DataTransfer-objekt för att simulera nya input.files
  const dataTransfer = new DataTransfer();
  selectedFiles.forEach(file => dataTransfer.items.add(file));
  fileInput.files = dataTransfer.files;
});

function renderPreviews() {
  previewContainer.innerHTML = "";

  selectedFiles.forEach((file, index) => {
    const fileElement = document.createElement("div");
    fileElement.classList.add("file-item");

    const fileName = document.createElement("span");
    fileName.textContent = file.name;

    const removeBtn = document.createElement("button");
    removeBtn.innerText = "X";
    removeBtn.addEventListener("click", () => {
      selectedFiles.splice(index, 1);
      renderPreviews();

      const dataTransfer = new DataTransfer();
      selectedFiles.forEach(file => dataTransfer.items.add(file));
      fileInput.files = dataTransfer.files;
    });

    fileElement.appendChild(fileName);
    fileElement.appendChild(removeBtn);
    previewContainer.appendChild(fileElement);
  });
}

let dropZone = document.getElementById("dropZone");

dropZone.addEventListener("click", () => {
  fileInput.click();
});