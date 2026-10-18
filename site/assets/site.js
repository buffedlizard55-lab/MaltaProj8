/* Progressive enhancement: per-table row filter. Everything else on the page
   works without JavaScript. */
(function () {
  "use strict";

  document.querySelectorAll("[data-filter-for]").forEach(function (input) {
    var table = document.getElementById(input.getAttribute("data-filter-for"));
    if (!table) { return; }
    var counter = document.querySelector('[data-count-for="' + table.id + '"]');
    var rows = Array.prototype.slice.call(table.tBodies[0].rows);

    function label() {
      if (counter) {
        counter.textContent = rows.length + " row" + (rows.length === 1 ? "" : "s");
      }
    }
    label();

    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      rows.forEach(function (row) {
        var hit = !q || row.textContent.toLowerCase().indexOf(q) !== -1;
        row.style.display = hit ? "" : "none";
        if (hit) { shown++; }
      });
      if (counter) {
        counter.textContent = shown + " of " + rows.length + " rows";
      }
    });
  });
})();
