document.addEventListener("DOMContentLoaded", () => {

  const addCaseBtn = document.getElementById("addCaseBtn");
  const caseModal = document.getElementById("caseModal");
  const viewModal = document.getElementById("viewModal");
  const closeButtons = document.querySelectorAll(".close-modal");
  const caseForm = document.getElementById("caseForm");
  const caseTableBody = document.querySelector("#caseTable tbody");
  const caseModalTitle = document.getElementById("caseModalTitle");
  const caseIndexInput = document.getElementById("caseIndex");
  const viewContent = document.getElementById("viewContent");

  let cases = JSON.parse(localStorage.getItem("cases") || "[]");

  
  const render = () => {
    caseTableBody.innerHTML = "";

    if (!cases.length) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td colspan="7" style="text-align:center; padding:18px; color:var(--muted)">
        No cases yet — click "Add Case" to create one.
      </td>`;
      caseTableBody.appendChild(tr);
      return;
    }

    cases.forEach((c, i) => {
      const esc = (s = "") =>
        String(s)
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;")
          .replace(/'/g, "&#039;");

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${i + 1}</td>
        <td>${esc(c.caseNumber)}</td>
        <td>${esc(c.plaintiff)} vs. ${esc(c.defendant)}</td>
        <td><span class="badge badge-warning">${esc(c.caseType)}</span></td>
        <td>${esc(c.hearingDate || "-")}</td>
        <td>${esc(c.judge)}</td>
        <td class="actions">
          <button class="btn btn-ghost small" data-action="view" data-index="${i}">View</button>
          <button class="btn btn-ghost small" data-action="edit" data-index="${i}">Edit</button>
          <button class="btn btn-delete small" data-action="delete" data-index="${i}">Delete</button>
        </td>`;
      caseTableBody.appendChild(tr);
    });
  };

  render();


  // Add Case Button

  addCaseBtn.addEventListener("click", () => {
    caseForm.reset();
    caseIndexInput.value = "";
    caseModalTitle.textContent = "Add New Case";

    caseModal.setAttribute("aria-hidden", "false");
    caseModal.style.display = "flex";
    document.body.style.overflow = "hidden";

    document.getElementById("caseNumber").focus();
  });


  // Close buttons for modals
 
  closeButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const parent = e.target.closest(".modal");
      parent.style.display = "none";
      parent.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    });
  });

  
  // Click outside modal to close
 
  document.addEventListener("click", (e) => {
    if (e.target === caseModal) {
      caseModal.style.display = "none";
      caseModal.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }
    if (e.target === viewModal) {
      viewModal.style.display = "none";
      viewModal.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }
  });


  // Form submit (Create / Update)

  caseForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const data = {
      caseNumber: caseForm.caseNumber.value.trim(),
      caseType: caseForm.caseType.value,
      plaintiff: caseForm.plaintiff.value.trim(),
      defendant: caseForm.defendant.value.trim(),
      judge: caseForm.judge.value.trim(),
      hearingDate: caseForm.hearingDate.value,
      remarks: caseForm.remarks.value.trim(),
    };

    if (!data.caseNumber || !data.plaintiff || !data.defendant || !data.judge) {
      alert("Please fill in Case Number, Plaintiff, Defendant and Assigned Judge.");
      return;
    }

    const idx = caseIndexInput.value;

    if (idx !== "") {
      cases[idx] = data;
    } else {
      cases.push(data);
    }

    localStorage.setItem("cases", JSON.stringify(cases));
    render();

    caseModal.style.display = "none";
    caseModal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  });


  // Delegated table actions
  
  caseTableBody.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;

    const action = btn.dataset.action;
    const idx = Number(btn.dataset.index);
    const c = cases[idx];

    const esc = (s = "") =>
      String(s)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

    if (action === "view") {
      viewContent.innerHTML = `
        <p><strong>Case Number:</strong> ${esc(c.caseNumber)}</p>
        <p><strong>Case Type:</strong> ${esc(c.caseType)}</p>
        <p><strong>Plaintiff:</strong> ${esc(c.plaintiff)}</p>
        <p><strong>Defendant:</strong> ${esc(c.defendant)}</p>
        <p><strong>Assigned Judge:</strong> ${esc(c.judge)}</p>
        <p><strong>Next Hearing:</strong> ${esc(c.hearingDate || "-")}</p>
        <p><strong>Remarks:</strong> ${esc(c.remarks || "-")}</p>
      `;
      viewModal.style.display = "flex";
      viewModal.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }

    if (action === "edit") {
      caseForm.caseNumber.value = c.caseNumber;
      caseForm.caseType.value = c.caseType;
      caseForm.plaintiff.value = c.plaintiff;
      caseForm.defendant.value = c.defendant;
      caseForm.judge.value = c.judge;
      caseForm.hearingDate.value = c.hearingDate;
      caseForm.remarks.value = c.remarks;

      caseIndexInput.value = idx;
      caseModalTitle.textContent = "Edit Case";

      caseModal.style.display = "flex";
      caseModal.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }

    if (action === "delete") {
      if (confirm(`Delete case "${c.caseNumber}"?`)) {
        cases.splice(idx, 1);
        localStorage.setItem("cases", JSON.stringify(cases));
        render();
      }
    }
  });
});
