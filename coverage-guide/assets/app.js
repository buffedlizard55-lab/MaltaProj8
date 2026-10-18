'use strict';
const input = document.querySelector('input[type="search"]');
if (input) {
  const rows = [...document.querySelectorAll('tbody tr')];
  const count = document.querySelector('.filter-count');
  function filter() {
    const query = input.value.trim().toLocaleLowerCase();
    let shown = 0;
    for (const row of rows) {
      row.hidden = !row.textContent.toLocaleLowerCase().includes(query);
      if (!row.hidden) shown++;
    }
    count.textContent = `${shown} of ${rows.length} entries shown${shown === 0 ? ' — try another search.' : '.'}`;
  }
  input.addEventListener('input', filter);
  filter();
}
