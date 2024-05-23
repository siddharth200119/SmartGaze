import React, { useState, useEffect } from 'react';
import './Clock.css';

const Clock = () => {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const intervalId = setInterval(() => {
      setTime(new Date());
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  const formattedDate = time.toLocaleDateString('en-US', options);
  const formattedTime = time.toLocaleTimeString('en-US');

  return (
    <div className="clock-widget">
      <div className="time">{formattedTime}</div>
      <div className="date">{formattedDate}</div>
    </div>
  );
};

export default Clock;
