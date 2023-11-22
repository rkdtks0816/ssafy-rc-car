import React, { useState, useEffect } from 'react';
import { selectState } from '../utils/Api';

function State(props) {
  const [powerState, setpowerState] = useState('img/OFF.png');
  const [cmdState, setcmdState] = useState('img/P.png');

  const checkState = async () => {
    const nowData = await selectState();
    if (nowData.mode == props.mode) {
      console.log(nowData)
      setpowerState(`img/${nowData.power}.png`)
      setcmdState(`img/${nowData.cmd}.png`)
    }
  }
  useEffect(() => {
    checkState();
    const updateState = setInterval(checkState, 100);
    return () => {
      clearInterval(updateState);
    };
  }, []);
  
  return (
    <div className='row'><div className='row align-items-center justify-content-around'>
        <div className='mt-3 col-2 text-center'>
          <img className='img-fluid' alt = "power" src = {powerState} />
        </div>
        <div className='mt-3 col-2 text-center'>
          <img className='img-fluid' alt = "cmd" src = {cmdState} />
        </div>
      </div>
    </div>
  );
}

export default State;
