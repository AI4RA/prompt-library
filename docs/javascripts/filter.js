(function () {
  function initFilter(container) {
    const tableId = container.getAttribute("data-table");
    const table = document.getElementById(tableId);
    if (!table) return;

    const rows = Array.from(table.querySelectorAll("tbody tr.component-row"));
    const qInput = container.querySelector("input.q");
    const catSel = container.querySelector("select.category");
    const domSel = container.querySelector("select.domain");
    const statSel = container.querySelector("select.status");
    const countEl = container.querySelector(".count");

    function apply() {
      const q = (qInput.value || "").trim().toLowerCase();
      const cat = catSel ? catSel.value : "";
      const dom = domSel ? domSel.value : "";
      const stat = statSel ? statSel.value : "";
      let shown = 0;
      rows.forEach((row) => {
        const text = (row.getAttribute("data-search") || "").toLowerCase();
        const rCat = row.getAttribute("data-category") || "";
        const rDom = row.getAttribute("data-domain") || "";
        const rStat = row.getAttribute("data-status") || "";
        const matches =
          (!q || text.indexOf(q) !== -1) &&
          (!cat || rCat === cat) &&
          (!dom || rDom === dom) &&
          (!stat || rStat === stat);
        row.classList.toggle("hidden", !matches);
        if (matches) shown++;
      });
      if (countEl) {
        countEl.textContent = shown + " of " + rows.length + " components";
      }
    }

    [qInput, catSel, domSel, statSel].forEach((el) => {
      if (!el) return;
      el.addEventListener("input", apply);
      el.addEventListener("change", apply);
    });
    apply();
  }

  function boot() {
    document.querySelectorAll(".component-filter").forEach(initFilter);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
  // MkDocs Material instant-navigation re-renders the page; rebind on hashchange.
  document.addEventListener("DOMContentLoaded", boot);
  if (window.document$) {
    window.document$.subscribe(boot);
  }
})();
