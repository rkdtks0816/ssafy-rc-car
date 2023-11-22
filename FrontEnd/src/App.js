import './App.css';
import React, { useState, useEffect } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import axios from 'axios';

const client = new W3CWebSocket('ws://192.168.110.165:8000/ws');

function App() {
  const d = ['mid', 'stop'];
  const dArr = [
    ['left', 'mid', 'right'],
    ['go', 'stop', 'back']
  ]
  const nowState = {
    onOff : `img/OFF.png`,
    DRP : `img/P.png` 
  }

  const [image, setImage] = useState('');
  const [data, setData] = useState(null);
  const [onOffImage, setOnOffImage] = useState('img/OFF.png');
  const [DRPImage, setDRPImage] = useState('img/P.png');
  const [mode, setMode] = useState('');
  const [cmd, setCmd] = useState('');

  const insertCommand = () => {
    axios.get(`http://192.168.110.164:3001/InsertCmd?mode=${mode}&cmd=${cmd}`);
  }

  const selectState = async () => {
    try {
      const response = await axios.get(`http://192.168.110.164:3001/SelectState`);
      setData(response.data);
      checkState(response.data);
    } catch (error) {
      console.log(error);
    }
  }
  const checkState = (nowData) => {
    nowState.onOff = `img/${nowData.power}.png`
    nowState.DRP = `img/${nowData.gear}.png`
    setOnOffImage(nowState.onOff);
    setDRPImage(nowState.DRP);
  }
  const keyCommand = (axis, direction) => {
    let nowD;
    if (d[axis] === dArr[axis][direction]) {
      return;
    }
    if (d[axis] === dArr[axis][1]) {
      nowD = dArr[axis][direction];
    }
    else {
      nowD = dArr[axis][1];
    }
    setCmd(nowD);
    insertCommand();
    d[axis] = nowD;
  }
  const handleKeyUp = (event) => {
    switch (event.key) {
      case 'ArrowUp':
        keyCommand(1, 0);
        break;
      case 'ArrowDown':
        keyCommand(1, 2);
        break;
      case 'ArrowLeft':
        keyCommand(0, 0);
        break;
      case 'ArrowRight':
        keyCommand(0, 2);
        break;
      default:
        // 다른 키 릴리즈 시 실행할 코드
        break;
    }
  }

  useEffect(() => {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      const imageData = message.data;
      setImage('data:image/jpeg;base64,' + imageData);
    };
    // 초기 렌더링 시 함수 실행
    selectState();
    const updateState = setInterval(selectState, 100);

    // 컴포넌트가 마운트되면 이벤트 리스너를 추가합니다.
    document.addEventListener('keyup', handleKeyUp);

    // 컴포넌트가 언마운트되면 이벤트 리스너를 제거합니다.
    return () => {
      document.removeEventListener('keyup', handleKeyUp);
      clearInterval(updateState);
    };
  }, []);
  
  return (
    <div className="App mx-auto">
      <header className='row justify-content-center'>
        <img className='col-2 img-fluid' alt = 'logo' src = 'img/logo.png' />
      </header>
      <main className='row'>
        {image && <div className='row mx-auto picam'>        
          <img className='img-fluid' src={image} alt="Streamed Image" />
        </div>}
        {data && <div className='row align-items-center justify-content-around'>
          <div className='mt-3 col-2 text-center'>
            <img className='img-fluid' alt = "onOff" src = {onOffImage} />
          </div>
          <div className='mt-3 col-2 text-center'>
            <img className='img-fluid' alt = "DRP" src = {DRPImage} />
          </div>
        </div>}
        <div className='mt-3 text-center d-flex justify-content-around'>
          <div className=''>
            <div onClick={() => insertCommand(dArr[1][0])} className='ctl-btn'>▲</div>
            <div onClick={() => insertCommand(dArr[1][1])} className='ctl-btn'>★</div>
            <div onClick={() => insertCommand(dArr[1][2])} className='ctl-btn'>▼</div>
          </div>
          <div className='d-flex align-items-center'>
            <div onClick={() => insertCommand(dArr[0][0])} className='ctl-btn'>◀</div>
            <div onClick={() => insertCommand(dArr[0][1])} className='ctl-btn'>★</div>
            <div onClick={() => insertCommand(dArr[0][2])} className='ctl-btn'>▶</div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
