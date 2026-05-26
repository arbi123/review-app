document.addEventListener("DOMContentLoaded", () => {
  const reportField = document.getElementById("report");
  const wordCountEl = document.getElementById("word-count");
  if (reportField && wordCountEl) {
    const updateCount = () => {
      const words = reportField.value.trim().split(/\s+/).filter(Boolean);
      wordCountEl.textContent = words.length;
      wordCountEl.classList.toggle("over", words.length > 100);
    };
    reportField.addEventListener("input", updateCount);
    updateCount();
  }

  document.querySelectorAll("[data-image-preview]").forEach((input) => {
    const previewId = input.getAttribute("data-image-preview");
    const preview = document.getElementById(previewId);
    if (!preview) return;
    const uploadLabel = input.closest(".file-upload");
    const uploadText = uploadLabel?.querySelector(".file-upload-text strong");
    input.addEventListener("change", () => {
      const file = input.files[0];
      if (!file) {
        preview.innerHTML = "";
        preview.classList.add("hidden");
        if (uploadText) uploadText.textContent = "Click to upload";
        return;
      }
      if (uploadText) uploadText.textContent = file.name;
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        preview.classList.remove("hidden");
      };
      reader.readAsDataURL(file);
    });
  });
});
