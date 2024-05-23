import React, { useState, useEffect } from 'react';
import { WEATHER_API_URL, WEATHER_API_KEY } from './api.js';
import "./current.css"

const CurrentWeather = ({ city }) => {
  const [currentWeather, setCurrentWeather] = useState(null);
  
useEffect(() => {
    if (city) {
      // Extract latitude and longitude from the provided city string
      const [lat, lon] = city.split(" ");
      
      // Fetch weather data
      const weatherAPIUrl = `${WEATHER_API_URL}/weather?lat=${lat}&lon=${lon}&appid=${WEATHER_API_KEY}&units=metric`;
      fetch(weatherAPIUrl)
        .then((response) => response.json())
        .then((weatherResponse) => {
          setCurrentWeather(weatherResponse);
        })
        .catch((err) => console.log(err));
    }
  }, [city]);

//{currentWeather.city}
  return (
    <div className="container">
      {currentWeather && (
        <div className="weather">
          <div className="top">
            <div>
               <p className="city"> {currentWeather.name}, {currentWeather.sys.country} </p>
               
               <p className="weather-description">
                 {currentWeather.weather[0].description}
               </p>
             </div>
             <img
              alt="weather"
              className="weather-icon"
              src={`/icons/${currentWeather.weather[0].icon}.png`}
            />
          </div>
          <div className="bottom">
            <p className="temperature">
              {Math.round(currentWeather.main.temp)}°C
            </p>
            <div className="details">
              <div className="parameter-row">
                <span className="para-label top"> details </span>
              </div>
              <div className="parameter-row">
                <span className="para-label">feels like </span>
                <span className="para-value">
                  {Math.round(currentWeather.main.feels_like)}°C
                </span>
              </div>
              <div className="parameter-row">
                <span className="para-label"> wind</span>
                <span className="para-value">
                  {currentWeather.wind.speed} m/s
                </span>
              </div>
              <div className="parameter-row">
                <span className="para-label"> humidity</span>
                <span className="para-value">
                  {currentWeather.main.humidity}%
                </span>
              </div>
              <div className="parameter-row">
                <span className="para-label"> pressure</span>
                <span className="para-value">
                  {currentWeather.main.pressure}hpa
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CurrentWeather;



// import React, { useState, useEffect } from 'react';
// import { WEATHER_API_URL, WEATHER_API_KEY } from '../../api';
// import "./current.css"

// const CurrentWeather = ({ city }) => {
//   const [currentWeather, setCurrentWeather] = useState(null);
//   //const [forecast, setForecast] = useState(null);

// //   useEffect(() => {
// //     if (city) {
// //       // Extract latitude and longitude from city (modify as needed)
// //       const [lat, lon] = city.split(" ");
// //       const currentWeatherFetch = fetch(
// //         `${WEATHER_API_URL}/weather?lat=${lat}&lon=${lon}&appid=${WEATHER_API_KEY}&units=metric`
// //       );
// //       const forecastFetch = fetch(
// //         `${WEATHER_API_URL}/forecast?lat=${lat}&lon=${lon}&appid=${WEATHER_API_KEY}&units=metric`
// //       );

// //       Promise.all([currentWeatherFetch, forecastFetch])
// //         .then(async (responses) => {
// //           const weatherResponse = await responses[0].json();
// //           const forecastResponse = await responses[1].json();

// //           setCurrentWeather({ city, ...weatherResponse });
// //           setForecast({ city, ...forecastResponse });
// //         })
// //         .catch((err) => console.log(err));
// //     }
// //   }, [city]);
// useEffect(() => {
//     if (city) {
//       // Extract latitude and longitude from the provided city string
//       const [lat, lon] = city.split(" ");
      
//       // Fetch weather data
//       const weatherAPIUrl = `${WEATHER_API_URL}/weather?lat=${lat}&lon=${lon}&appid=${WEATHER_API_KEY}&units=metric`;
//       fetch(weatherAPIUrl)
//         .then((response) => response.json())
//         .then((weatherResponse) => {
//           setCurrentWeather(weatherResponse);
//         })
//         .catch((err) => console.log(err));
//     }
//   }, [city]);

// //{currentWeather.city}
//   return (
//     <div className="container">
//       {currentWeather && (
//         <div className="weather">
//           <div className="top">
//             <div>
//                <p className="city"> {currentWeather.name}, {currentWeather.sys.country} </p>
               
//                <p className="weather-description">
//                  {currentWeather.weather[0].description}
//                </p>
//              </div>
//              <img
//               alt="weather"
//               className="weather-icon"
//               src={`icons/${currentWeather.weather[0].icon}.png`}
//             />
//           </div>
//           <div className="bottom">
//             <p className="temperature">
//               {Math.round(currentWeather.main.temp)}°C
//             </p>
//             <div className="details">
//               <div className="parameter-row">
//                 <span className="para-label top"> details </span>
//               </div>
//               <div className="parameter-row">
//                 <span className="para-label">feels like </span>
//                 <span className="para-value">
//                   {Math.round(currentWeather.main.feels_like)}°C
//                 </span>
//               </div>
//               <div className="parameter-row">
//                 <span className="para-label"> wind</span>
//                 <span className="para-value">
//                   {currentWeather.wind.speed} m/s
//                 </span>
//               </div>
//               <div className="parameter-row">
//                 <span className="para-label"> humidity</span>
//                 <span className="para-value">
//                   {currentWeather.main.humidity}%
//                 </span>
//               </div>
//               <div className="parameter-row">
//                 <span className="para-label"> pressure</span>
//                 <span className="para-value">
//                   {currentWeather.main.pressure}hpa
//                 </span>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default CurrentWeather;
//---

// import React, { useState, useEffect } from "react";
// import Search from "../search/Search";
// import { WEATHER_API_URL, WEATHER_API_KEY } from "../../api";
// import "./current.css"
// const CurrentWeather = () => {
//   const [currentWeather, setCurrentWeather] = useState(null);
//   const [forecast, setForecast] = useState(null);

//   useEffect(() => {
//     // Move the API call logic here
//     // You can call this effect whenever the search data changes

//     // Define a function for making the API calls
//     const fetchWeatherData = (lat, lon) => {
//       const currentWeatherFetch = fetch(
//         `${WEATHER_API_URL}/weather?lat=${23.2156}&lon=${72.6369}&appid=${WEATHER_API_KEY}&units=metric`
//       );
//       const forecastFetch = fetch(
//         `${WEATHER_API_URL}/forecast?lat=${lat}&lon=${lon}&appid=${WEATHER_API_KEY}&units=metric`
//       );

//       Promise.all([currentWeatherFetch, forecastFetch])
//         .then(async (responses) => {
//           const weatherResponse = await responses[0].json();
//           const forecastResponse = await responses[1].json();

//           setCurrentWeather({ city: searchValue, ...weatherResponse }); // Update with searchValue
//           setForecast({ city: searchValue, ...forecastResponse }); // Update with searchValue
//         })
//         .catch((err) => console.log(err));
//     };

//     // Use the searchValue or coordinates from the search component
//     // For this example, I'm using searchValue as a placeholder
//     const searchValue = "Gandhinagar,Gujrat"; // Replace this with the actual selected search value

//     if (searchValue) {
//       // Extract latitude and longitude from searchValue (modify as needed)
//       const [lat, lon] = searchValue.split(" ");
//       fetchWeatherData(lat, lon);
//     }
//   }, []); // You can add searchValue to the dependency array if needed

//   return (
//     <div className="container">
//       <Search />
//       {currentWeather && currentWeather.weather && currentWeather.weather[0] ? (
//         <div className="weather">
//           {/* Render the weather information here */}
//           <div className="top">
//             <div>
//               <p className="city"> {currentWeather.city} </p>
//               <p className="weather-description">
//                 {currentWeather.weather[0].description}
//               </p>
//             </div>
//             <img
//               alt="weather"
//               className="weather-icon"
//               src={`icons/${currentWeather.weather[0].icon}.png`}
//             />
//           </div>
//           <div className="bottom">
//             <p className="temperature">
//               {Math.round(currentWeather.main.temp)}°C
//             </p>
//             <div className="details">
//               <div className="parameter-row">
//                 <span className="para-label top"> details </span>
//               </div>
//               <div className="parameter-row">
//                 <span className="para-label">feels like </span>
//                 <span className="para-value">
//                   {Math.round(currentWeather.main.feels_like)}°C
//                 </span>
//               </div>
//               <div className="parameter-row">
//                 <span className="para-label"> wind</span>
//                 <span className="para-value">
//                   {currentWeather.wind.speed} m/s
//                 </span>
//               </div>
//               <div className="parameter-row">
//                 <span className="para-label"> humidity</span>
//                 <span className="para-value">
//                   {currentWeather.main.humidity}%
//                 </span>
//               </div>
//               <div className="parameter-row">
//                 <span className="para-label"> pressure</span>
//                 <span className="para-value">
//                   {currentWeather.main.pressure}hpa
//                 </span>
//               </div>
//             </div>
//           </div>
//         </div>
//       ) : (
//         <p>Loading...</p>
//       )}
//     </div>
//   );
// };

// export default CurrentWeather;



//--------

// import "./current.css"
// import React, { useState, useEffect } from "react";
// import Search from './components/search/Search';
// import { WEATHER_API_URL, WEATHER_API_KEY } from './api';
// import { useState } from 'react';

// const CurrentWeather = ({data}) => {
//     return (
//         <div className="weather">
//             <div className="top">
//                 <div>
//                     <p className="city"> {data.city} </p>
//                     <p className="weather-description"> {data.weather[0].description}</p>

//                 </div>
//                 <img alt="weather" className="weather-icon" src={`icons/${data.weather[0].icon}.png` }/>
//             </div>
//             <div className="bottom">
//                 <p className="temperature">{Math.round(data.main.temp)}°C</p>
//                 <div className="details">
//                     <div className="parameter-row">
//                         <span className="para-label top"> details </span>
//                     </div>
//                     <div className="parameter-row">
//                         <span className="para-label">feels like  </span>
//                         <span className="para-value">{Math.round(data.main.feels_like)}°C  </span>
//                     </div>
//                     <div className="parameter-row">
//                         <span className="para-label"> wind</span>
//                         <span className="para-value">{data.wind.speed} m/s </span>
//                     </div>
//                     <div className="parameter-row">
//                         <span className="para-label"> humidity</span>
//                         <span className="para-value">{data.main.humidity}% </span>
//                     </div>
//                     <div className="parameter-row">
//                         <span className="para-label"> pressure</span>
//                         <span className="para-value">{data.main.pressure}hpa </span>
//                     </div>
//                 </div>

//             </div>

//         </div>


//     );
// }
// export default CurrentWeather;



//ORIGINAL

// import "./current.css"

// const CurrentWeather = ({data}) => {
//     return (
//         <div className="weather">
//             <div className="top">
//                 <div>
//                     <p className="city"> {data.city} </p>
//                     <p className="weather-description"> {data.weather[0].description}</p>

//                 </div>
//                 <img alt="weather" className="weather-icon" src={`icons/${data.weather[0].icon}.png` }/>
//             </div>
//             <div className="bottom">
//                 <p className="temperature">{Math.round(data.main.temp)}°C</p>
//                 <div className="details">
//                     <div className="parameter-row">
//                         <span className="para-label top"> details </span>
//                     </div>
//                     <div className="parameter-row">
//                         <span className="para-label">feels like  </span>
//                         <span className="para-value">{Math.round(data.main.feels_like)}°C  </span>
//                     </div>
//                     <div className="parameter-row">
//                         <span className="para-label"> wind</span>
//                         <span className="para-value">{data.wind.speed} m/s </span>
//                     </div>
//                     <div className="parameter-row">
//                         <span className="para-label"> humidity</span>
//                         <span className="para-value">{data.main.humidity}% </span>
//                     </div>
//                     <div className="parameter-row">
//                         <span className="para-label"> pressure</span>
//                         <span className="para-value">{data.main.pressure}hpa </span>
//                     </div>
//                 </div>

//             </div>

//         </div>


//     );
// }
// export default CurrentWeather;