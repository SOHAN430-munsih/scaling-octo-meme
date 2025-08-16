const form = document.getElementById('predict-form');
const resultCard = document.getElementById('result');
const resultJson = document.getElementById('result-json');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  resultCard.classList.add('hidden');
  resultJson.textContent = 'Loading...';

  try {
    // You can switch to '/predict' if you like; both are supported.
    const res = await fetch('/api/predict', { method: 'POST', body: fd });
    const data = await res.json();
    resultCard.classList.remove('hidden');
    resultJson.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    resultCard.classList.remove('hidden');
    resultJson.textContent = 'Error: ' + err.message;
  }
});
