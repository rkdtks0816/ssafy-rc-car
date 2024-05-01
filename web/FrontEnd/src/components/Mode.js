import React from 'react';
import Mouse from './Mouse'
import Keyboard from './Keyboard'

function Mode(props) {
  return (
    <div>
        <div className='row  align-items-center justify-content-around'>
          <div onClick={() => props.setMode('mouse')} className='col-2 mode-btn'>
            <img className='img-fluid' alt = "mouseMode" src = 'img/mouseMode.png' />
          </div>
          <div onClick={() => props.setMode('keyboard')} className='col-2 mode-btn'>
            <img className='img-fluid' alt = "keyboardMode" src = 'img/keyboardMode.png' />
          </div>
          <div onClick={() => props.setMode('controller')} className='col-2 mode-btn'>
            <img className='img-fluid' alt = "controllerMode" src = 'img/controllerMode.png' />
          </div>
          <div onClick={() => props.setMode('mic')} className='col-2 mode-btn'>
            <img className='img-fluid' alt = "micMode" src = 'img/micMode.png' />
          </div>
        </div>
        {props.mode == 'mouse' && <Mouse />}
        {props.mode == 'keyboard' && <Keyboard />}
        {props.mode == 'controller' && <div className='row justify-content-center'>
            <img className='img-fluid explanation' alt = "controllerImg" src = 'img/controllerImg.png' />
          </div>}
        {props.mode == 'mic' && <div className='row justify-content-center'>
            <img className='img-fluid explanation' alt = "micImg" src = 'img/micImg.png' />
          </div>}
    </div>
  );
}

export default Mode;
