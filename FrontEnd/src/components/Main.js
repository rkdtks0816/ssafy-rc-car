import React, { useState, useEffect } from 'react';
import Mode from './Mode'
import Streaming from './Streaming'
import State from './State'

function Main() {
  const [mode, setMode] = useState('mouse');
  return (
    <div className="Main mx-auto">
      <header className='row justify-content-center'>
        <img className='col-2 img-fluid' alt = 'logo' src = 'img/logo.png' />
      </header>
      <main className='row'>
        <Streaming />
        <State mode = {mode}/>
        <Mode mode = {mode} setMode = {setMode}/>
      </main>
    </div>
  );
}

export default Main;
