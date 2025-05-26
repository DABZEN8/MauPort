const titleInput = document.getElementById("titleInput");
const titleDisplay = document.getElementById("titleDisplay");
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("fileList");

// Uppdatera rubriken dynamiskt
if (titleInput && titleDisplay) {
    titleInput.addEventListener("input", () => {
        const value = titleInput.value.trim();
        if (value !== "") {
            titleDisplay.textContent = value;
            titleDisplay.classList.remove("hidden");
        } else {
            titleDisplay.classList.add("hidden");
        }
    });
}

// Klicka på dropzone = trigga file input
if (dropZone && fileInput) {
    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("dragover", e => {
        e.preventDefault();
        dropZone.style.backgroundColor = "#333";
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.style.backgroundColor = "#1e1e1e";
    });

    dropZone.addEventListener("drop", e => {
        e.preventDefault();
        dropZone.style.backgroundColor = "#1e1e1e";

        const dt = new DataTransfer();
        Array.from(fileInput.files).forEach(file => dt.items.add(file));
        Array.from(e.dataTransfer.files).forEach(file => dt.items.add(file));

        fileInput.files = dt.files;
        updateFileList();
    });

    fileInput.addEventListener("change", updateFileList);
}

function updateFileList() {
    if (!fileInput || !fileList) return;

    fileList.innerHTML = "";
    Array.from(fileInput.files).forEach((file, index) => {
        const div = document.createElement("div");
        div.textContent = file.name;

        const removeBtn = document.createElement("button");
        removeBtn.textContent = "X";
        removeBtn.type = "button";
        removeBtn.addEventListener("click", () => removeFile(index));

        div.appendChild(removeBtn);
        fileList.appendChild(div);
    });
}

function removeFile(indexToRemove) {
    const dt = new DataTransfer();
    Array.from(fileInput.files).forEach((file, index) => {
        if (index !== indexToRemove) {
            dt.items.add(file);
        }
    });
    fileInput.files = dt.files;
    updateFileList();
}