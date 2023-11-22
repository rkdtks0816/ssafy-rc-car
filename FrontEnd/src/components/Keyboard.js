import React, { useState, useEffect } from 'react';
import { insertCommand } from '../utils/Api'

function Keyboard() {
  const [nowP, setNowP] = useState('OFF'); 
  
  const powerToggle = () => {
    if (nowP == 'OFF') setNowP('ON');
    else setNowP('OFF');
    insertCommand('mouse', nowP);
  }

  const handleKeyUp = (event) => {
    switch (event.key) {
      case 'q':
        insertCommand('mouse', 'rgl');
        break;
      case 'w':
        insertCommand('mouse', 'rg');
        break;
      case 'e':
        insertCommand('mouse', 'rgr');
        break;
      case 'a':
        insertCommand('mouse', 'rl');
        break;
      case 's':
        insertCommand('mouse', 'rs');
        break;
      case 'd':
        insertCommand('mouse', 'rr');
        break;
      case 'z':
        insertCommand('mouse', 'rbl');
        break;
      case 'x':
        insertCommand('mouse', 'rb');
        break;
      case 'c':
        insertCommand('mouse', 'rbr');
        break;
      case 't':
        insertCommand('mouse', 'su');
        break;
      case 'g':
        powerToggle();
        break;
      case 'b':
        insertCommand('mouse', 'sd');
          break;
      case 'u':
        insertCommand('mouse', 'cgl');
        break;
      case 'i':
        insertCommand('mouse', 'cg');
        break;
      case 'o':
        insertCommand('mouse', 'cgr');
        break;
      case 'j':
        insertCommand('mouse', 'cl');
        break;
      case 'k':
        insertCommand('mouse', 'cs');
        break;
      case 'l':
        insertCommand('mouse', 'cr');
        break;
      case 'm':
        insertCommand('mouse', 'cbl');
        break;
      case ',':
        insertCommand('mouse', 'cb');
        break;
      case '.':
        insertCommand('mouse', 'cbr');
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
      document.removeEventListener('keyup', handleKeyUp)
    };
  }, []);
  
  return (
    <div className='row justify-content-center'>
      <img className='img-fluid explanation' alt = "keyboardImg" src = 'img/keyboardImg.png' />
    </div>
  );
}

export default Keyboard;
