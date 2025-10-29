// script.js - CRUD with localStorage + modal control
(function () {
  // Elements
  const addCaseBtn = document.getElementById('addCaseBtn');
  const caseModal = document.getElementById('caseModal');
  const viewModal = document.getElementById('viewModal');
  const closeCaseModalBtns = document.querySelectorAll('.close-modal');
  const caseForm = document.getElementById('caseForm');
  const caseTableBody = document.querySelector('#caseTable tbody');
  const caseModalTitle = document.getElementById('caseModalTitle');
  const caseIndexInput = document.getElementById('caseIndex');
  const viewContent = document.getElementById('viewContent');

  // Data
  let cases = JSON.parse(localStorage.getItem('cases') || '[]');

  // Utilities
  function save() {
    localStorage.setItem('cases', JSON.stringify(cases));
  }

  function openModal(modal) {
    modal.setAttribute('aria-hidden', 'false');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
  function closeModal(modal) {
    modal.setAttribute('aria-hidden', 'true');
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }

  // Render table
  function render() {
    caseTableBody.innerHTML = '';
    if (!cases.length) {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td colspan="7" style="text-align:center; padding:18px; color:var(--muted)">No cases yet — click "Add Case" to create one.</td>`;
      caseTableBody.appendChild(tr);
      return;
    }

    cases.forEach((c, i) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${i + 1}</td>
        <td>${escapeHtml(c.caseNumber)}</td>
        <td>${escapeHtml(c.plaintiff)} vs. ${escapeHtml(c.defendant)}</td>
        <td><span class="badge badge-warning">${escapeHtml(c.caseType)}</span></td>
        <td>${escapeHtml(c.hearingDate || '-')}</td>
        <td>${escapeHtml(c.judge)}</td>
        <td class="actions">
          <button class="btn btn-ghost small" data-action="view" data-index="${i}">View</button>
          <button class="btn btn-ghost small" data-action="edit" data-index="${i}">Edit</button>
          <button class="btn btn-delete small" data-action="delete" data-index="${i}">Delete</button>
        </td>`;
      caseTableBody.appendChild(tr);
    });
  }


  function escapeHtml(s = '') {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Handlers
  addCaseBtn.addEventListener('click', () => {
    caseForm.reset();
    caseIndexInput.value = '';
    caseModalTitle.textContent = 'Add New Case';
    openModal(caseModal);
    document.getElementById('caseNumber').focus();
  });

  // Close all close-modal buttons
  closeCaseModalBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const parent = e.target.closest('.modal');
      if (parent) closeModal(parent);
    });
  });

  // Click outside to close modals
  window.addEventListener('click', (e) => {
    if (e.target === caseModal) closeModal(caseModal);
    if (e.target === viewModal) closeModal(viewModal);
  });

  // Form submit (create or update)
  caseForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = {
      caseNumber: caseForm.caseNumber.value.trim(),
      caseType: caseForm.caseType.value,
      plaintiff: caseForm.plaintiff.value.trim(),
      defendant: caseForm.defendant.value.trim(),
      judge: caseForm.judge.value.trim(),
      hearingDate: caseForm.hearingDate.value,
      remarks: caseForm.remarks.value.trim()
    };

    // Basic required fields
    if (!data.caseNumber || !data.plaintiff || !data.defendant || !data.judge) {
      alert('Please fill in Case Number, Plaintiff, Defendant and Assigned Judge.');
      return;
    }

    const idx = caseIndexInput.value;
    if (idx !== '') {
      cases[Number(idx)] = data;
    } else {
      cases.push(data);
    }
    save();
    render();
    closeModal(caseModal);
  });

  // Delegated actions for view/edit/delete
  caseTableBody.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    const action = btn.dataset.action;
    const idx = Number(btn.dataset.index);
    if (action === 'view') {
      const c = cases[idx];
      viewContent.innerHTML = `
        <p><strong>Case Number:</strong> ${escapeHtml(c.caseNumber)}</p>
        <p><strong>Case Type:</strong> ${escapeHtml(c.caseType)}</p>
        <p><strong>Plaintiff:</strong> ${escapeHtml(c.plaintiff)}</p>
        <p><strong>Defendant:</strong> ${escapeHtml(c.defendant)}</p>
        <p><strong>Assigned Judge:</strong> ${escapeHtml(c.judge)}</p>
        <p><strong>Next Hearing:</strong> ${escapeHtml(c.hearingDate || '-')}</p>
        <p><strong>Remarks:</strong> ${escapeHtml(c.remarks || '-')}</p>
      `;
      openModal(viewModal);
    } else if (action === 'edit') {
      const c = cases[idx];
      caseForm.caseNumber.value = c.caseNumber;
      caseForm.caseType.value = c.caseType;
      caseForm.plaintiff.value = c.plaintiff;
      caseForm.defendant.value = c.defendant;
      caseForm.judge.value = c.judge;
      caseForm.hearingDate.value = c.hearingDate;
      caseForm.remarks.value = c.remarks;
      caseIndexInput.value = idx;
      caseModalTitle.textContent = 'Edit Case';
      openModal(caseModal);
    } else if (action === 'delete') {
      const confirmed = confirm(`Delete case "${cases[idx].caseNumber}"? This cannot be undone.`);
      if (confirmed) {
        cases.splice(idx, 1);
        save();
        render();
      }
    }
  });

  // init
  render();
})();
