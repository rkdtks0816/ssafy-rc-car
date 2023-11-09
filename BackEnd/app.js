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
    port: '3306',
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
  const { Cmd } = req.query;
  try {
    const connection = GetConnection();
    const query = `INSERT INTO command(time, cmd_string, arg_string, is_finish) VALUES (CURRENT_TIMESTAMP(), '${Cmd}', 0, 0)`;

    connection.query(query, (error, results, fields) => {
      if (error) {
        console.error(`Error performing 'InsertCmd('${Cmd}')': ${error.message}`);
        res.status(500).json({ error: 'Error performing database operation' });
      } else {
        console.log(`Succeed to do 'InsertCmd('${Cmd}')'`);
        res.status(200).json({ message: 'Command inserted successfully' });
      }
    });

    connection.end();
  } catch (error) {
    console.error(`Error performing 'InsertCmd('${Cmd}')': ${error.message}`);
    res.status(500).json({ error: 'Error performing database operation' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
