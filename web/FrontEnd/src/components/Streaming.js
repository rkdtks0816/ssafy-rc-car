import React, { useState, useEffect } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';

const client = new W3CWebSocket('ws://192.168.110.165:8000/ws');

function Streaming() {
  const [image, setImage] = useState('');
  useEffect(() => {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      const imageData = message.data;
      setImage('data:image/jpeg;base64,' + imageData);
    };
  }, [image]);
  return (
    <div>
      {image && <div className='row mx-auto picam'>        
        <img className='img-fluid' src={image} alt="Streamed Image" />
      </div>}
    </div>
  );
}

export default Streaming;
