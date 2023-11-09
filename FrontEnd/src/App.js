import './App.css';
import React, { useState, useEffect } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import axios from 'axios';

const client = new W3CWebSocket('ws://192.168.110.165:8000/ws');

function App() {
  const [image, setImage] = useState('');

  useEffect(() => {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      const imageData = message.data;
      setImage('data:image/jpeg;base64,' + imageData);
    };
    const handleKeyDown = (event) => {
      console.log(event.key)
      // 여기에서 키보드 이벤트를 처리합니다.
      if (event.key === 'ArrowUp') {
        // API 호출로 RC 카를 전진시킵니다.
        axios.get('http://192.168.110.164:3001/InsertCmd?Cmd=go');
      } else if (event.key === 'ArrowDown') {
        // API 호출로 RC 카를 후진시킵니다.
        axios.get('http://192.168.110.164:3001/InsertCmd?Cmd=back');
      } else if (event.key === 'ArrowLeft') {
        // API 호출로 RC 카를 왼쪽으로 회전시킵니다.
        axios.get('http://192.168.110.164:3001/InsertCmd?Cmd=left');
      } else if (event.key === 'ArrowRight') {
        // API 호출로 RC 카를 오른쪽으로 회전시킵니다.
        axios.get('http://192.168.110.164:3001/InsertCmd?Cmd=right');
      }
    };
    const handleKeyUp = (event) => {
      console.log(event.key)
      // 여기에서 키보드 이벤트를 처리합니다.
      if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
        // API 호출로 RC 카를 전진시킵니다.
        axios.get('http://192.168.110.164:3001/InsertCmd?Cmd=stop');
      } else if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        // API 호출로 RC 카를 왼쪽으로 회전시킵니다.
        axios.get('http://192.168.110.164:3001/InsertCmd?Cmd=mid');
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    }
  }, []);

  return (
    <div className="App">
      <header>
        <h3>GamZa King</h3>
      </header>
      <main className='row main-container'>
        <div className='col-3'>
          <div>
            속도
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
