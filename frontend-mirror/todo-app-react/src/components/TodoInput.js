import React, { useState, useEffect } from 'react';
import Todolist from './TodoList';

function TodoInput() {
  const [listTodo, setListTodo] = useState([]);

  useEffect(() => {
    // Fetch data from the API when the component mounts
    fetch('https://jsonplaceholder.typicode.com/todos')
      .then(response => response.json())
      .then(data => {
        // Update state with fetched data
        setListTodo(data);
      })
      .catch(error => {
        console.error('There was a problem fetching data:', error);
      });
  }, []); // Empty dependency array ensures that the effect runs only once on component mount

  return (
    <div className="main-container">
      <div className="center-container">
        <h1 className="app-heading">TO-DO LIST</h1>
        <hr className="horizontal-line" />
        <table className="todo-table">
          <thead>
            <tr>
              <th>Task</th>
              <th>Due Date</th>
            </tr>
          </thead>
          <tbody>
            {listTodo.filter(todo => todo.complete === 0) // Filter tasks where complete variable is 0
              .map(todo => (
                <Todolist key={todo.id} title={todo.title} dueDate={todo.dueDate} />
                // <tr key={todo.id}>
                //    <td>{todo.title}</td>
                //    <td>{todo.dueDate}</td>
                // </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default TodoInput;


// import React, { useState, useEffect } from 'react';
// import Todolist from './TodoList';

// function TodoInput() {
//   const [listTodo, setListTodo] = useState([]);

//   useEffect(() => {
//     // Fetch data from the API when the component mounts
//     fetch('https://jsonplaceholder.typicode.com/todos')
//       .then(response => response.json())
//       .then(data => {
//         // Update state with fetched data
//         setListTodo(data);
//       })
//       .catch(error => {
//         console.error('There was a problem fetching data:', error);
//       });
//   }, []); // Empty dependency array ensures that the effect runs only once on component mount

//   return (
//     <div className="main-container">
//       <div className="center-container" style={{ textAlign: "center" }} >
//         <h1 className="app-heading">TO-DO LIST</h1>
//         <hr style={{ width: "370px" }} />
//         <div className="todo-list">
//           {listTodo.filter(todo => todo.complete === 0) // Filter tasks where complete variable is 0
//             .map(todo => (
//               <Todolist key={todo.id} title={todo.title} dueDate={todo.dueDate} />
//             ))}
//         </div>
//       </div>
//     </div>
//   );
// }

// export default TodoInput;