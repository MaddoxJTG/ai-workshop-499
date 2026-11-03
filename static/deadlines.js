// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
function showDeadline(row, cell, opportunity) {
  const daysLeft = opportunity.days_left + 1;
  let label;
  let className;

  if (daysLeft < 0) {
    label = "Overdue";
    className = "deadline-label deadline-overdue";
  } else if (daysLeft === 0) {
    label = "Due today";
    className = "deadline-label deadline-today";
  } else if (daysLeft <= 7) {
    label = `Due in ${daysLeft} ${daysLeft === 1 ? "day" : "days"}`;
    className = "deadline-label deadline-upcoming";
  } else {
    return;
  }

  const badge = document.createElement("span");
  badge.className = className;
  badge.textContent = label;
  cell.appendChild(badge);
}
