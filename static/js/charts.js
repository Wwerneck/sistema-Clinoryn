document.addEventListener("DOMContentLoaded", () => {
  const node = document.getElementById("dashboard-chart-data");
  if (!node || typeof Chart === "undefined") return;
  const data = JSON.parse(node.textContent);
  const common = { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { usePointStyle: true, boxWidth: 8, color: "#667085", font: { family: "Inter" } } } } };
  const specialtyCanvas = document.getElementById("specialtiesChart");
  if (specialtyCanvas) new Chart(specialtyCanvas, { type: "bar", data: { labels: data.specialties.labels, datasets: [{ data: data.specialties.values, backgroundColor: "#3b82f6", borderRadius: 6, maxBarThickness: 38 }] }, options: { ...common, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false } }, y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: "#eef2f6" } } } } });
  const statusCanvas = document.getElementById("statusChart");
  if (statusCanvas) new Chart(statusCanvas, { type: "doughnut", data: { labels: data.statuses.labels, datasets: [{ data: data.statuses.values, backgroundColor: ["#22a06b", "#3b82f6", "#f59e0b", "#8b5cf6", "#ef6b6b", "#94a3b8"], borderWidth: 0, spacing: 3 }] }, options: { ...common, cutout: "70%" } });
});
