// Sample dispatch slots
const dispatchSlots = [
  { time: "8:00 AM", job: "Melton - Mowing", status: "Scheduled" },
  { time: "10:30 AM", job: "Bacchus Marsh - Bin Pickup", status: "Pending" },
  { time: "1:00 PM", job: "NDIS Visit - Caroline Springs", status: "Confirmed" }
];

function renderDispatchCalendar() {
  const container = document.getElementById("dispatchCalendar");
  container.innerHTML = "";

  dispatchSlots.forEach(slot => {
    const div = document.createElement("div");
    div.className = "dispatch-slot";
    div.innerHTML = `<strong>${slot.time}</strong>: ${slot.job} <em>(${slot.status})</em>`;
    container.appendChild(div);
  });
}

renderDispatchCalendar();
