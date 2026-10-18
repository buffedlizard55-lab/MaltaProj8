const input = document.querySelector('#search');
if (input) {
  const rows = [...document.querySelectorAll('tbody tr')];
  const count = document.querySelector('#result-count');
  input.addEventListener('input', () => {
    const query = input.value.trim().toLowerCase();
    for (const row of rows) row.hidden = !row.textContent.toLowerCase().includes(query);
    count.textContent = `${rows.filter(row => !row.hidden).length} of ${rows.length} entries shown`;
  });
}
