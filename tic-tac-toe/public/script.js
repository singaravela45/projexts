const boxes = document.querySelectorAll(".box");
const resetbtn = document.querySelector("#reset");
const player1score = document.querySelector(".player1score");
const player2score = document.querySelector(".player2score");
const tiescore = document.querySelector(".tiescore");
const player1_score = document.querySelector(".player1_score");
const player2_score = document.querySelector(".player2_score");
let player1_wins = 0;
let player2_wins = 0;
let tie = 0;
const results = document.querySelector(".results");
let isactive = true;

const check_array = Array(9).fill(false);
const player1_array = Array(9).fill(false);
const player2_array = Array(9).fill(false);
let checkPlayer1turn = true;
//check tie
const checkTie = (array) => {
  for (var i = 0; i < 9; i++) {
    if (!array[i]) return;
  }
  tie++;
  tiescore.textContent = tie;
  results.textContent="It is a draw !!"
  results.style.opacity = "1";
  setTimeout(() => {
    resetboard();
    isactive = true;
    results.style.opacity = "0";
  }, 1000);
};
// check wins
const checkwin = (array) => {
  if (
    (array[0] && array[1] && array[2]) ||
    (array[3] && array[4] && array[5]) ||
    (array[6] && array[7] && array[8]) ||
    (array[0] && array[3] && array[6]) ||
    (array[1] && array[4] && array[7]) ||
    (array[2] && array[5] && array[8]) ||
    (array[0] && array[4] && array[8]) ||
    (array[2] && array[4] && array[6])
  ) {
    return true;
  }
  return false;
};
boxes.forEach((box) => {
  box.addEventListener("click", () => {
    if (!isactive) return;
    const idx = parseInt(box.dataset.index, 10);
    if (check_array[idx]) {
      console.log("error");
      return;
    }
    check_array[idx] = true;
    if (checkPlayer1turn) {
      checkPlayer1turn = false;
      box.innerHTML = "<p>X</p>";
      player1_score.classList.add("turnfinder");
      player2_score.classList.remove("turnfinder");
      player1_array[idx] = true;
      if (checkwin(player1_array)) {
        player1_wins++;
        player1score.textContent = player1_wins;
        results.textContent = "player 1 wins !";
        results.style.opacity = "1";
        isactive = false;
        setTimeout(() => {
          resetboard();
          isactive = true;
          results.style.opacity = "0";
        }, 1000);
        return;
      }
      checkTie(check_array);
    } else {
      checkPlayer1turn = true;
      box.innerHTML = "<p>O</p>";
      player1_score.classList.remove("turnfinder");
      player2_score.classList.add("turnfinder");
      player2_array[idx] = true;
      if (checkwin(player2_array)) {
        isactive = false;
        player2_wins++;
        player2score.textContent = player2_wins;
        results.textContent = "player 2 wins !";
        results.style.opacity = "1";
        setTimeout(() => {
          resetboard();
          isactive = true;
          results.style.opacity = "0";
        }, 1000);
        return;
      }
      checkTie(check_array);
    }
  });
});
const resetboard = () => {
  boxes.forEach((box) => {
    box.innerHTML = " ";
    player1_array.fill(false);
    player2_array.fill(false);
    check_array.fill(false);
    checkPlayer1turn = true;
    player1_score.classList.remove("turnfinder");
    player2_score.classList.add("turnfinder");
  });
};

resetbtn.addEventListener("click", () => {
  resetboard();

});
