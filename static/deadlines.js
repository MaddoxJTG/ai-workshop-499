// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
function showDeadline(row, cell, opportunity) {
  if (opportunity.days_left < 0) {
    row.classList.add("overdue");
    cell.classList.add("deadline-overdue");
    addDeadlineLabel(cell, "deadline-label-overdue", "Overdue");
  } else if (opportunity.days_left === 0) {
    row.classList.add("due-soon");
    cell.classList.add("deadline-due-soon");
    cell.classList.add("deadline-due-today");
    addDeadlineLabel(cell, "deadline-label-due-today", "Due Today");
  } else if (opportunity.days_left <= 7) {
    row.classList.add("due-soon");
    cell.classList.add("deadline-due-soon");
    addDeadlineLabel(cell, "deadline-label-due-soon", "Due in " + opportunity.days_left + " days");
  }
}

function addDeadlineLabel(cell, className, text) {
  const label = document.createElement("span");
  label.className = "deadline-label " + className;
  label.textContent = text;
  cell.appendChild(label);
}
