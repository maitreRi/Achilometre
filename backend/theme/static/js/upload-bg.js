document.addEventListener("DOMContentLoaded", () => {
  const uploadBtn = document.getElementById('upload-bg-btn');
  const uploadInput = document.getElementById('upload-bg-input');

  uploadBtn.addEventListener('click', () => {
    uploadInput.click();
  });

  uploadInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file || !file.type.startsWith('image/')) {
      alert('Veuillez sélectionner une image valide.');
      return;
    }

    const reader = new FileReader();
    reader.onload = function (event) {
      const imageDataUrl = event.target.result;
      document.body.style.backgroundImage = `url('${imageDataUrl}')`;
      document.body.style.backgroundSize = 'cover';
      document.body.style.backgroundPosition = 'center center';
      document.body.style.backgroundRepeat = 'no-repeat';
      localStorage.setItem('userBackground', imageDataUrl);
    };

    reader.readAsDataURL(file);
  });

  const savedBg = localStorage.getItem('userBackground');
  if (savedBg) {
    document.body.style.backgroundImage = `url('${savedBg}')`;
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundPosition = 'center center';
    document.body.style.backgroundRepeat = 'no-repeat';
  }
});
