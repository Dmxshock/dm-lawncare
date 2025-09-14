const systemChecks = [
  { module: "Quote Engine", status: "✅ Online" },
  { module: "Dispatch Planner", status: "✅ Online" },
  { module: "Email Trigger", status: "⚠️ Delayed" }
];

function renderMonitoringStatus() {
  const container = document.getElementById("monitoringStatus");
  container.innerHTML = "";

  systemChecks.forEach(check => {
    const div = document.createElement("div");
    div.className = "monitoring-check";
    div.innerHTML = `<strong>${check.module}</strong>: ${check.status}`;
    container.appendChild(div);
  });
}

renderMonitoringStatus();
