import express from "express";
import path from 'path';
const app = express();

app.use(express.static( "/projexts/tic-tac-toe/public"));

app.listen(8000, () => {
  console.log("server is up");
});
