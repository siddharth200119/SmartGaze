import React from 'react';

function Todolist(props) {
  const currentDate = new Date();
  const dueDate = new Date(props.dueDate);

  const isPastDue = dueDate < currentDate;
  const blockColor = isPastDue ? 'red' : 'inherit';

  return (
    <li className="list-item" style={{ backgroundColor: blockColor }}>
      <div className="title">{props.title}</div>
      <div className="due-date">Due Date: {props.dueDate}</div>
    </li>
  );
}

export default Todolist;



// import React from 'react';

// function Todolist(props) {
//   return (
//     <li className="list-item">
//       <div className="title">{props.title}</div>
//       <div className="due-date">Due Date: {props.dueDate}</div>
//     </li>
//   );
// }

// export default Todolist;

