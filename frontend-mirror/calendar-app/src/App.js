import React, { useState } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";

function App() {
  const [date, changeDate] = useState(new Date());

  function changeValue(val) {
    changeDate(val);
  }

  return (
    <body>
      <div>
        <Calendar onChange={changeValue} value={date} />
      </div>
    </body>
  );
}
export default App;