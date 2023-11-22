const express = require('express');
const cors = require('cors');
const app = express();
const port = 3001;

const mysql = require('mysql2');

app.use(cors({
  origin: '*', // 모든 출처 허용 옵션. true 를 써도 된다.
}));

// DB 연동
function GetConnection() {
  const connection = mysql.createConnection({
    host: '192.168.110.164',
    port: 3306,  // 문자열이 아닌 숫자로 지정
    user: 'root',
    password: '1234',
    database: 'RC',
  });

  connection.connect((err) => {
    if (err) throw err;
    console.log('Connected to MySQL server!');
  });

  return connection;
}

// 명령어 삽입
app.get('/InsertCmd', (req, res) => {
  const { mode, cmd } = req.query;
  try {
    const connection = GetConnection();
    const query = `INSERT INTO command(time, mode, cmd, is_finish) VALUES (CURRENT_TIMESTAMP(), '${mode}', '${cmd}', 0)`;

    connection.query(query, (error, results, fields) => {
      if (error) {
        console.error(`Error performing 'InsertCmd('${mode}', '${cmd}')': ${error.message}`);
        res.status(500).json({ error: 'Error performing database operation' });
      } else {
        console.log(`Succeed to do 'InsertCmd('${mode}', '${cmd}')'`);
        res.status(200).json({ message: 'Command inserted successfully' });
      }
    });

    connection.end();
  } catch (error) {
    console.error(`Error performing 'InsertCmd('${mode}', '${cmd}')': ${error.message}`);
    res.status(500).json({ error: 'Error performing database operation' });
  }
});

// 현재 상태
app.get('/InsertState', (req, res) => {
  const { mode, cmd,  power } = req.query;
  try {
    const connection = GetConnection();
    const query = `INSERT INTO state(time, mode, cmd, power, is_finish) VALUES (CURRENT_TIMESTAMP(), '${mode}', '${cmd}', '${power}', 0)`;

    connection.query(query, (error, results, fields) => {
      if (error) {
        console.error(`Error performing 'InsertState('${mode}', '${cmd}', '${power}')': ${error.message}`);
        res.status(500).json({ error: 'Error performing database operation' });
      } else {
        console.log(`Succeed to do 'InsertState('${mode}', '${cmd}', '${power}')'`);
        res.status(200).json({ message: 'State inserted successfully' });
      }
    });

    connection.end();
  } catch (error) {
    console.error(`Error performing 'InsertState('${mode}', '${cmd}', '${power}')': ${error.message}`);
    res.status(500).json({ error: 'Error performing database operation' });
  }
});

// 현재 상태 조회
app.get('/SelectState', (req, res) => {
  try {
    const connection = GetConnection();
    const query = `SELECT * FROM state ORDER BY time DESC LIMIT 1`;

    connection.query(query, (error, results, fields) => {
      if (error) {
        console.error(`Error performing 'SelectState': ${error.message}`);
        res.status(500).json({ error: 'Error performing database operation' });
      } else {
        // 결과가 없거나 is_finish가 1인 경우
        if (!results.length || results[0].is_finish === 1) {
          res.json({ message: 'No pending state' });
          connection.end();  // 연결 종료 위치 변경
          return;
        }

        // 상태 완료 표시
        const updateQuery = 'UPDATE state SET is_finish = 1 WHERE is_finish = 0';
        connection.query(updateQuery, (error, updateResults, fields) => {
          if (error) {
            console.error(`Error performing 'UpdateState': ${error.message}`);
            res.status(500).json({ error: 'Error performing database operation' });
          } else {
            console.log('UpdateState successful');
            // 데이터를 응답으로 전송하거나 필요에 따라 수정
            res.json(results[0]);
          }
          
          connection.end();  // 연결 종료 위치 변경
        });
      }
    });
  } catch (error) {
    console.error(`Error performing 'SelectState': ${error.message}`);
    res.status(500).json({ error: 'Error performing database operation' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
