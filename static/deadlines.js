// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
function showDeadline(row, cell, opportunity) {
  if (opportunity.days_left < 0) {
    row.classList.add("overdue");
    cell.classList.add("deadline-overdue");

    const label = document.createElement("span");
    label.className = "deadline-label";
    label.textContent = "Overdue";
    cell.appendChild(label);
  }
}
