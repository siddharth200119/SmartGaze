import React, { useState, useEffect } from 'react';
import "./Dashboard.css"
import GridLayout from 'react-grid-layout';
import Calendar from "react-calendar";
import News from '../Widgets/News/News.jsx';
import Clock from '../Widgets/Clock/Clock.js';
import Weather from '../Widgets/Weather/current-weather.js';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import { useParams } from 'react-router-dom';
import SpotifyPlayer from 'react-spotify-web-playback';
import ToDOList from '../Widgets/ToDoList/ToDoList.jsx';

function Dashboard() {
  const {data} = useParams()
  const data_json = JSON.parse(data)
  const username = data_json.user_data.username;
  const layout = data_json.layout;
  const toDOList = data_json.top_10_todo;
  const authCode = data_json.user_data.spotify_access_token;
  const news_pref = data_json.topics

  const [isKPressed, setIsKPressed] = useState(false);
  const [isSnapshotKPressed, setIsSnapshotKPressed] = useState(false);

  useEffect(() => {
    const handleKeyDown = (event) => {
      const play = document.getElementsByClassName("ButtonRSWP rswp__toggle _ControlsButtonRSWP __3hmsj")[0];
      const next = document.getElementsByClassName("ButtonRSWP _ControlsButtonRSWP __3hmsj")[2];
      if (event.key === 'k') {
        setIsKPressed((prevState) => !prevState);
        play.click()
      }
      if(event.key === "l") {
        next.click()
      }
      if (event.key === 'f') {
        setIsSnapshotKPressed((prevState) => !prevState);
        setTimeout(() => {
          setIsSnapshotKPressed((prevState) => !prevState);
        }, 1500);
      }
    };
    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  const date = new Date();

  const city = "23.2156 72.6369";

  return (
    <div className="container">
      <h1 className='userName'>Welcome {username}!</h1>
      <GridLayout className="layout" layout={layout}  cols={3} width={document.body.offsetWidth}>
        <div style={{"display": "flex", "alignItems": "flex-start", "justifyContent": "center"}} key="widget3">
          <Clock/>
        </div>
        <div style={{"display": "flex", "alignItems": "flex-start", "justifyContent": "center"}} key="widget2">
          <News preferences={news_pref}/>
        </div>
        <div style={{"display": "flex", "alignItems": "flex-start", "justifyContent": "center"}} key="widget1">
          <Weather city={city}/>
        </div>
        <div style={{"display": "flex", "alignItems": "flex-end", "justifyContent": "center"}} key="widget4">
          <Calendar value={date}/>
        </div>
        <div style={{"display": "flex", "alignItems": "flex-start", "justifyContent": "center"}} key="widget5">
            <ToDOList list={toDOList}/>
        </div>
      </GridLayout>
      {(authCode !== undefined)? (
        <div className={isKPressed ? 'spotify show' : 'spotify'}>
        <SpotifyPlayer
            styles={{bgColor: "black", color: 'white'}}
            token={authCode}
            uris={['spotify:artist:6HQYnRM4OzToCYPpVBInuU']}
        />
      </div>
      
      ): (
        <div></div>
      )}
      <div className={isSnapshotKPressed ? 'snapshot-popup show' : 'snapshot-popup'}>
        Snapshot Saved!
      </div>
    </div>
  );
}

export default Dashboard;
