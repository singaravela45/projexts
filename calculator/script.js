const display = document.querySelector(".display");
const button = document.querySelector(".button");
const numbers = document.querySelectorAll(".number");
const oper = document.querySelectorAll(".oper");
const clear = document.querySelector(".clear");
const enter = document.querySelector(".enter");
let num1 = 0;
let num2 = 0;
let operation = "";
let secondnum = false;
clear.addEventListener("click", () => {
  display.value = "";
  num1 = 0;
  num2 = 0;
  operation = "";
  secondnum = false;
});
numbers.forEach((number) => {
  number.addEventListener("click", (event) => {
    if (secondnum) {
      display.value = "";
      secondnum = false;
    }
    addtodisplay(number.innerHTML);
  });
});
oper.forEach((operator) => {
  operator.addEventListener("click", (event) => {
    operation = event.target.innerHTML;
    num1 = Number(display.value);
    display.value = display.value + operation;
    secondnum = true;
  });
});
enter.addEventListener("click", () => {
  num2 = Number(display.value);
  display.value = evaluate(num1, num2, operation);
});
function addtodisplay(value) {
  display.value += value;
}
function evaluate(num1, num2, operation) {
  switch (operation) {
    case "+":
      return num1 + num2;
    case "-":
      return num1 - num2;
    case "*":
      return num1 * num2;
    case "/":
      return num1 / num2;
    default:
      break;
  }
}
