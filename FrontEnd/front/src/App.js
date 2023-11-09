import './App.css';
import React, { useState, useEffect } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import GaugeChart from 'react-gauge-chart'

const client = new W3CWebSocket('ws://192.168.110.165:8000/ws');

function App() {
  const [image, setImage] = useState('');
  const gaugeData = {
      value: 30, // 변경 가능한 값
      maxValue: 100,
  };

  useEffect(() => {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      const imageData = message.data;
      setImage('data:image/jpeg;base64,' + imageData);
    };
  }, []);

  return (
    <div className="App">
      <header>
        <h3>GamZa King</h3>
      </header>
      <main className='row main-container'>
        <div className='col-3'>
          <div style={{width: '100%', height: '100%'}}>
              <GaugeChart id="gauge-chart1" 
                  nrOfLevels={30} 
                  percent={gaugeData.value / gaugeData.maxValue} 
              />
          </div>
          <div>
            온도
          </div>
        </div>
        <div className='col-6'>        
          {image && <img className='img-fluid' src={image} alt="Streamed Image" />}
        </div>
        <div className='col-3'></div>
      </main>
    </div>
  );
}

export default App;
