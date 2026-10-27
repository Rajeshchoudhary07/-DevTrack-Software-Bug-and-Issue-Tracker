const $ = (id) => document.getElementById(id);
const backdrop = $("modalBackdrop");
let toastTimer;
function toast(message) {
  $("toast").textContent = message;
  $("toast").classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => $("toast").classList.remove("show"), 2600);
}
function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
function statusClass(status) {
  return status === "In Progress" ? "status-progress" : status === "Resolved" ? "status-resolved" : "status-open";
}
async function api(url, options = {}) {
  const response = await fetch(url, {headers: {"Content-Type":"application/json"}, ...options});
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || "Request failed.");
  return data;
}
async function loadIssues() {
  const params = new URLSearchParams();
  if ($("statusFilter").value) params.set("status", $("statusFilter").value);
  if ($("priorityFilter").value) params.set("priority", $("priorityFilter").value);
  if ($("searchInput").value.trim()) params.set("q", $("searchInput").value.trim());
  try {
    const result = await api(`/api/issues?${params}`);
    const all = (await api("/api/issues")).items;
    $("totalCount").textContent = all.length;
    $("openCount").textContent = all.filter(x => x.status === "Open").length;
    $("progressCount").textContent = all.filter(x => x.status === "In Progress").length;
    $("resolvedCount").textContent = all.filter(x => x.status === "Resolved").length;
    if (!result.items.length) {
      $("issueList").innerHTML = '<div class="empty">No issues found. Create an issue to get started.</div>';
      return;
    }
    $("issueList").innerHTML = result.items.map(issue => `
      <article class="issue-row">
        <div>
          <div class="issue-title">#${issue.id} · ${esc(issue.title)}</div>
          <div class="issue-desc">${esc(issue.description || "No description provided.")}</div>
          <div class="meta">
            <span class="pill ${statusClass(issue.status)}">${esc(issue.status)}</span>
            <span class="pill priority-${issue.priority.toLowerCase()}">${esc(issue.priority)}</span>
            <span class="assignee">Assigned to ${esc(issue.assignee)}</span>
          </div>
        </div>
        <div class="row-actions">
          <button data-edit="${issue.id}">Edit</button>
          <button class="delete" data-delete="${issue.id}">Delete</button>
        </div>
      </article>`).join("");
  } catch (error) {
    $("issueList").innerHTML = `<div class="empty">${esc(error.message)} Make sure the Flask server is running.</div>`;
  }
}
function openModal(issue = null) {
  $("issueForm").reset();
  $("issueId").value = issue?.id || "";
  $("modalTitle").textContent = issue ? `Edit issue #${issue.id}` : "Create an issue";
  $("title").value = issue?.title || "";
  $("description").value = issue?.description || "";
  $("priority").value = issue?.priority || "Medium";
  $("status").value = issue?.status || "Open";
  $("assignee").value = issue?.assignee || "";
  $("formError").textContent = "";
  backdrop.hidden = false;
  $("title").focus();
}
function closeModal() { backdrop.hidden = true; }
$("newIssueBtn").addEventListener("click", () => openModal());
$("closeModal").addEventListener("click", closeModal);
$("cancelModal").addEventListener("click", closeModal);
backdrop.addEventListener("click", e => { if (e.target === backdrop) closeModal(); });
document.addEventListener("keydown", e => { if (e.key === "Escape") closeModal(); });
$("issueForm").addEventListener("submit", async e => {
  e.preventDefault();
  const id = $("issueId").value;
  const payload = {
    title: $("title").value.trim(), description: $("description").value.trim(),
    priority: $("priority").value, status: $("status").value,
    assignee: $("assignee").value.trim() || "Unassigned"
  };
  try {
    await api(id ? `/api/issues/${id}` : "/api/issues", {
      method: id ? "PATCH" : "POST", body: JSON.stringify(payload)
    });
    closeModal();
    toast(id ? "Issue updated successfully." : "Issue created successfully.");
    await loadIssues();
  } catch (error) { $("formError").textContent = error.message; }
});
$("issueList").addEventListener("click", async e => {
  const editId = e.target.dataset.edit;
  const deleteId = e.target.dataset.delete;
  try {
    if (editId) {
      const issue = await api(`/api/issues/${editId}`);
      openModal(issue);
    }
    if (deleteId && confirm(`Delete issue #${deleteId}? This cannot be undone.`)) {
      await api(`/api/issues/${deleteId}`, {method:"DELETE"});
      toast("Issue deleted.");
      await loadIssues();
    }
  } catch (error) { toast(error.message); }
});
["statusFilter","priorityFilter"].forEach(id => $(id).addEventListener("change", loadIssues));
let searchDebounce;
$("searchInput").addEventListener("input", () => { clearTimeout(searchDebounce); searchDebounce = setTimeout(loadIssues, 220); });
loadIssues();
