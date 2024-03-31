import React from 'react';
import './App.css';
import { Responsive, WidthProvider } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import TodoInput from './components/TodoInput';

const ResponsiveGridLayout = WidthProvider(Responsive);

function App() {
  const layout = [
    { i: 'todoInput', x: 12, y: 12, w: 12, h: 4 },
    { i: 'todoList', x: 12, y: 12, w: 12, h: 4 },
  ];

  return (
    <div className="container">
      <ResponsiveGridLayout className="layout" layout={layout}  cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}>
        <div key="todoInput">
          <TodoInput />
        </div>
      </ResponsiveGridLayout>
    </div>
  );
}

export default App;


// import React from 'react';
// import './App.css';
// import TodoInput from './components/TodoInput';
// import Todolist from './components/TodoList';
// // import GridLayout from "react-grid-layout";

// function App() {

//   return (
//     <div className="container">
//       <TodoInput />
//       <Todolist/>

//     </div>
//   );
// }

// export default App;
