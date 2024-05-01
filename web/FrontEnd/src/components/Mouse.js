import React, { useState, useEffect } from 'react';
import { insertCommand } from '../utils/Api'

function Mouse() {
  const [nowP, setNowP] = useState('OFF'); 
  
  const powerToggle = () => {
    const newPowerState = nowP === 'OFF' ? 'ON' : 'OFF';
    setNowP(newPowerState);
    // 파워 상태를 바로 전송
    insertCommand('keyboard', newPowerState);
  };
  
  
  return (
    <div className='mt-3 text-center row justify-content-around'>
      <div className='col-4'>
        <div className='row'>
          <div onClick={() => insertCommand('mouse', 'rgl')} className='col ctl-btn'>◤</div>
          <div onClick={() => insertCommand('mouse', 'rg')} className='col ctl-btn'>▲</div>
          <div onClick={() => insertCommand('mouse', 'rgr')} className='col ctl-btn'>◥</div>
        </div>
        <div className='row'>
          <div onClick={() => insertCommand('mouse', 'rl')} className='col ctl-btn'>◀</div>
          <div onClick={() => insertCommand('mouse', 'rs')} className='col ctl-btn'>🐶</div>
          <div onClick={() => insertCommand('mouse', 'rr')} className='col ctl-btn'>▶</div>
        </div>
        <div className='row'>
          <div onClick={() => insertCommand('mouse', 'rbl')} className='col ctl-btn'>◣</div>
          <div onClick={() => insertCommand('mouse', 'rb')} className='col ctl-btn'>▼</div>
          <div onClick={() => insertCommand('mouse', 'rbr')} className='col ctl-btn'>◢</div>
        </div>
      </div>
      <div className='col-2'>
        <div className='row justify-content-center'>
          <div onClick={() => insertCommand('mouse', 'su')} className='ctl-btn'>▲</div>
          <div onClick={powerToggle} className='ctl-btn'>⭕</div>
          <div onClick={() => insertCommand('mouse', 'sd')} className='ctl-btn'>▼</div>
        </div>
      </div>
      <div className='col-4'>
        <div className='row'>
          <div onClick={() => insertCommand('mouse', 'cgl')} className='col ctl-btn'>◤</div>
          <div onClick={() => insertCommand('mouse', 'cg')} className='col ctl-btn'>▲</div>
          <div onClick={() => insertCommand('mouse', 'cgr')} className='col ctl-btn'>◥</div>
        </div>
        <div className='row'>
          <div onClick={() => insertCommand('mouse', 'cl')} className='col ctl-btn'>◀</div>
          <div onClick={() => insertCommand('mouse', 'cs')} className='col ctl-btn'>📸</div>
          <div onClick={() => insertCommand('mouse', 'cr')} className='col ctl-btn'>▶</div>
        </div>
        <div className='row'>
          <div onClick={() => insertCommand('mouse', 'cbl')} className='col ctl-btn'>◣</div>
          <div onClick={() => insertCommand('mouse', 'cb')} className='col ctl-btn'>▼</div>
          <div onClick={() => insertCommand('mouse', 'cbr')} className='col ctl-btn'>◢</div>
        </div>
      </div>
    </div>
  );
}

export default Mouse;
