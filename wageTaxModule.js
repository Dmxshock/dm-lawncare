const jobsCompleted = [
  { operator: "Damien", service: "mowing", base: 60, travel: 25 },
  { operator: "Damien", service: "bin", base: 30, travel: 0 }
];

function calculateWages() {
  let total = 0;
  jobsCompleted.forEach(job => {
    total += job.base + job.travel;
  });

  const gst = total * 0.1;
  const net = total - gst;

  const summary = `
    <p><strong>Total Earned:</strong> $${total.toFixed(2)}</p>
    <p><strongGST (10%):</strong> $${gst.toFixed(2)}</p>
    <p><strong>Net Income:</strong> $${net.toFixed(2)}</p>
  `;

  document.getElementById("wageSummary").innerHTML = summary;
}

calculateWages();
