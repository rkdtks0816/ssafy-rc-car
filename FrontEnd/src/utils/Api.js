import axios from 'axios';

const insertCommand = (mode, cmd) => {
  axios.get(`http://192.168.110.164:3001/InsertCmd?mode=${mode}&cmd=${cmd}`);
}

const insertState = (mode, cmd, power) => {
  axios.get(`http://192.168.110.164:3001/InsertState?mode=${mode}&cmd=${cmd}&power=${power}`);
}
const selectState = async () => {
  try {
    const response = await axios.get(`http://192.168.110.164:3001/SelectState`);
    return response.data
  } catch (error) {
    console.log(error);
  }
}

export {
  selectState,
  insertState,
  insertCommand
};
