import React from 'react';

function Todolist(props) {
  const currentDate = new Date();
  const dueDate = new Date(props.dueDate);

  const isPastDue = dueDate < currentDate;
  const blockColor = isPastDue ? 'red' : 'inherit';

  return (
    <tr className="list-item" style={{ backgroundColor: blockColor }}>
      <td>{props.title}</td>
      <td>{props.dueDate}</td>
    </tr>
  );
}

export default Todolist;


