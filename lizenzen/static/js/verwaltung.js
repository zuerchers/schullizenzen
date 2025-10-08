// ===== CSRF-Token =====
function getCsrfToken() {
  const el = document.querySelector("[name=csrfmiddlewaretoken]");
  return el ? el.value : "";
}

// ===== Modal Handling =====
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    const form = modal.querySelector("form");
    if (form) form.reset();
    modal.style.display = "block";
  }
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.style.display = "none";
}

// ===== Toast Feedback =====
function showToast(msg) {
  let t = document.getElementById("toast");
  if (!t) {
    t = document.createElement("div");
    t.id = "toast";
    t.className = "toast";
    document.body.appendChild(t);
  }
  t.innerText = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2000);
}

// ===== Tabellenfilter =====
function bindFilters(tableSel) {
  const table = document.querySelector(tableSel);
  if (!table) return;
  const inputs = table.querySelectorAll("thead .filter input");

  inputs.forEach((input) => {
    input.addEventListener("input", () => {
      const rows = table.querySelectorAll("tbody tr");
      rows.forEach((row) => {
        const cells = row.querySelectorAll("td");
        let show = true;
        inputs.forEach((f, idx) => {
          if (
            f.value &&
            cells[idx] &&
            !cells[idx].innerText.toLowerCase().includes(f.value.toLowerCase())
          ) {
            show = false;
          }
        });
        row.style.display = show ? "" : "none";
      });
    });
  });
}

// ===== Sortieren =====
function bindSorting(tableSel) {
  const table = document.querySelector(tableSel);
  if (!table) return;
  const heads = table.querySelectorAll("thead th");

  heads.forEach((th, idx) => {
    const headerText = th.innerText.trim().toLowerCase();
    if (headerText === "aktionen" || headerText === "") return;

    th.addEventListener("click", () => {
      const tbody = table.querySelector("tbody");
      const rows = Array.from(tbody.querySelectorAll("tr"));
      const asc = !th.classList.contains("asc");

      rows.sort((a, b) => {
        const A = (a.children[idx]?.innerText || "").trim();
        const B = (b.children[idx]?.innerText || "").trim();
        return asc ? A.localeCompare(B) : B.localeCompare(A);
      });

      tbody.innerHTML = "";
      rows.forEach((r) => tbody.appendChild(r));

      heads.forEach((h) => {
        h.classList.remove("asc", "desc");
        const s = h.querySelector(".sort-indicator");
        if (s) s.remove();
      });

      th.classList.add(asc ? "asc" : "desc");
      const ind = document.createElement("span");
      ind.className = "sort-indicator";
      ind.innerText = asc ? "↑" : "↓";
      th.appendChild(ind);
    });
  });
}

// ===== Inline Edit Handling =====
function bindInline(tableSel, baseUrl) {
  const table = document.querySelector(tableSel);
  if (!table) return;

  table.querySelectorAll("tbody tr").forEach((row) => {
    const editBtn = row.querySelector(".edit-btn");
    const saveBtn = row.querySelector(".save-btn");
    const cancelBtn = row.querySelector(".cancel-btn");
    const deleteBtn = row.querySelector(".delete-btn");

    if (!editBtn || !saveBtn || !cancelBtn) return;

    // --- Edit starten ---
    editBtn.addEventListener("click", () => {
      row.classList.add("editing");
      row.querySelectorAll(".display").forEach((el) => (el.style.display = "none"));
      row.querySelectorAll(".edit").forEach((el) => {
        el.style.display = "inline-block";
        el.style.fontSize = "0.85rem";
        el.style.fontFamily = "inherit";
      });
      editBtn.style.display = "none";
      saveBtn.style.display = "";
      cancelBtn.style.display = "";
      if (deleteBtn) deleteBtn.style.display = "none";
    });

    // --- Abbrechen ---
    cancelBtn.addEventListener("click", () => {
      row.classList.remove("editing");
      row.querySelectorAll(".display").forEach((el) => (el.style.display = ""));
      row.querySelectorAll(".edit").forEach((el) => (el.style.display = "none"));
      editBtn.style.display = "";
      saveBtn.style.display = "none";
      cancelBtn.style.display = "none";
      if (deleteBtn) deleteBtn.style.display = "";
    });

    // --- Speichern ---
    saveBtn.addEventListener("click", async () => {
      const id = row.dataset.id;
      const fd = new FormData();
      row.querySelectorAll(".edit").forEach((input) => {
        if (input.name && !input.readOnly) fd.append(input.name, input.value);
      });

      const resp = await fetch(`/${baseUrl}/${id}/inline/update/`, {
        method: "POST",
        headers: { "X-CSRFToken": getCsrfToken() },
        body: fd,
      });

      if (resp.ok) {
        showToast("Änderungen gespeichert");
        setTimeout(() => location.reload(), 2000);
      } else {
        showToast("Fehler beim Speichern");
      }
    });

    // --- Löschen ---
    if (deleteBtn) {
      deleteBtn.addEventListener("click", () => {
        const modal = document.getElementById("deleteModal");
        modal.style.display = "block";
        const confirm = document.getElementById("confirmDeleteBtn");

        confirm.onclick = async () => {
          const resp = await fetch(`/${baseUrl}/${row.dataset.id}/inline/delete/`, {
            method: "POST",
            headers: { "X-CSRFToken": getCsrfToken() },
          });
          if (resp.ok) {
            modal.style.display = "none";
            showToast("Eintrag gelöscht");
            setTimeout(() => location.reload(), 2000);
          } else {
            showToast("Fehler beim Löschen");
          }
        };
      });
    }
  });
}

// ===== Modal-Create =====
function bindCreateForms() {
  document.querySelectorAll(".create-form").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const resp = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCsrfToken(),
          "X-Requested-With": "XMLHttpRequest",
        },
        body: data,
      });

      if (resp.ok) {
        const result = await resp.json();
        const modal = form.closest(".modal");
        const modalId = modal.id;

        if (/Lizenznehmer|Software|Kostentyp|Schuleinheit|Schulklasse/.test(modalId)) {
          let selectName = null;
          if (form.action.includes("lizenznehmer")) selectName = "lizenznehmer";
          if (form.action.includes("software")) selectName = "software";
          if (form.action.includes("kostentyp")) selectName = "kostentyp";
          if (form.action.includes("schuleinheit")) selectName = "schuleinheit";
          if (form.action.includes("schulklasse")) selectName = "schulklasse";

          if (selectName) {
            const select = document.querySelector(
              "#createVerwaltungModal select[name='" + selectName + "']"
            );
            if (select) {
              const opt = document.createElement("option");
              opt.value = result.id;
              opt.textContent = result.name;
              opt.selected = true;
              select.appendChild(opt);
            }
          }
          closeModal(modalId);
          openModal("createVerwaltungModal");
          showToast(`${result.name} wurde erstellt.`);
        } else {
          closeModal(modalId);
          showToast("Eintrag gespeichert.");
          setTimeout(() => location.reload(), 2000);
        }
      } else {
        showToast("Fehler beim Speichern");
      }
    });
  });
}

// ===== Klick außerhalb von Modal schließt es =====
window.addEventListener("click", (e) => {
  if (e.target.classList.contains("modal")) e.target.style.display = "none";
});

// ===== Init =====
document.addEventListener("DOMContentLoaded", () => {
  // Verwaltung
  bindFilters("#verwaltung-table");
  bindSorting("#verwaltung-table");
  bindInline("#verwaltung-table", "verwaltung");

  // FK-Tabellen
  const path = window.location.pathname.split("/").filter(Boolean)[0] || "";
  const fkBases = ["lizenznehmer", "software", "kostentyp", "schuleinheit", "schulklasse"];
  if (fkBases.includes(path.toLowerCase())) {
    bindFilters(".fk-table table");
    bindSorting(".fk-table table");
    bindInline(".fk-table table", path.toLowerCase());
  }

  bindCreateForms();
});
