import './App.css';
import React from 'react';
import NotAuth from './Screens/NotAuth';
import Dashboard from './Screens/Dashboard';
import {BrowserRouter, Routes, Route} from "react-router-dom"

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<NotAuth/>}/>
        <Route path="/users/:data?" element={<Dashboard/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
