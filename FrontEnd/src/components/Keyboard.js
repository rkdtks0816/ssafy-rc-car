import React, { useState, useEffect } from 'react';
import { insertCommand } from '../utils/Api'

function Keyboard() {
  const [nowP, setNowP] = useState('OFF'); 
  
  const powerToggle = () => {
    const newPowerState = nowP === 'OFF' ? 'ON' : 'OFF';
    setNowP(newPowerState);
    // 파워 상태를 바로 전송
    insertCommand('keyboard', newPowerState);
  };

  const handleKeyUp = (event) => {
    switch (event.key) {
      case 'q':
        insertCommand('keyboard', 'rgl');
        break;
      case 'w':
        insertCommand('keyboard', 'rg');
        break;
      case 'e':
        insertCommand('keyboard', 'rgr');
        break;
      case 'a':
        insertCommand('keyboard', 'rl');
        break;
      case 's':
        insertCommand('keyboard', 'rs');
        break;
      case 'd':
        insertCommand('keyboard', 'rr');
        break;
      case 'z':
        insertCommand('keyboard', 'rbl');
        break;
      case 'x':
        insertCommand('keyboard', 'rb');
        break;
      case 'c':
        insertCommand('keyboard', 'rbr');
        break;
      case 't':
        insertCommand('keyboard', 'su');
        break;
      case 'g':
        powerToggle();
        break;
      case 'b':
        insertCommand('keyboard', 'sd');
          break;
      case 'u':
        insertCommand('keyboard', 'cgl');
        break;
      case 'i':
        insertCommand('keyboard', 'cg');
        break;
      case 'o':
        insertCommand('keyboard', 'cgr');
        break;
      case 'j':
        insertCommand('keyboard', 'cl');
        break;
      case 'k':
        insertCommand('keyboard', 'cs');
        break;
      case 'l':
        insertCommand('keyboard', 'cr');
        break;
      case 'm':
        insertCommand('keyboard', 'cbl');
        break;
      case ',':
        insertCommand('keyboard', 'cb');
        break;
      case '.':
        insertCommand('keyboard', 'cbr');
        break;
      default:
        // 다른 키 릴리즈 시 실행할 코드
        break;
    }
  }

  useEffect(() => {
    document.addEventListener('keyup', handleKeyUp);
    // 컴포넌트가 언마운트되면 이벤트 리스너를 제거합니다.
    return () => {
      document.removeEventListener('keyup', handleKeyUp);
    };
  }, []);
  
  return (
    <div className='row justify-content-center'>
      <img className='img-fluid explanation' alt = "keyboardImg" src = 'img/keyboardImg.png' />
    </div>
  );
}

export default Keyboard;
