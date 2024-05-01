import React, { useState, useEffect } from 'react';
import Mode from './Mode'
import Streaming from './Streaming'
import State from './State'
import { insertState } from '../utils/Api'

function Main() {
  const [mode, setMode] = useState('mouse');
  const [power, setPower] = useState('OFF');
  useEffect(() => {
    insertState(mode, 'changeMode', power)
  }, [mode]);
  return (
    <div className="Main mx-auto">
      <header className='row justify-content-center'>
        <img className='col-2 img-fluid' alt = 'logo' src = 'img/logo.png' />
      </header>
      <main className='row'>
        <Streaming />
        <State mode = {mode} setMode = {setMode} setPower = {setPower}/>
        <Mode mode = {mode} setMode = {setMode}/>
      </main>
    </div>
  );
}

export default Main;
