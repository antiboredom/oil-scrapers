const lineTime = 1000;

let lines = [];
let index = 0;
let container = document.getElementById("app");

function showLine() {
  const line = lines[index];
  let el = document.createElement("p");
  el.textContent = `${index + 1} of ${lines.length}: ${line}`;

  container.appendChild(el);

  index += 1;
  if (index >= lines.length) index = 0;

  if (index % 10 === 0) {
    setTimeout(() => {
      app.innerHTML = "";
      showLine();
    }, lineTime);
  } else {
    setTimeout(showLine, lineTime);
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function showLineCharacters() {
  const line = `${index + 1} of ${lines.length}: ${lines[index]}`;
  const characters = line.split("");

  let el = document.createElement("p");
  container.appendChild(el);

  for (let i = 0; i < characters.length; i++) {
    let c = document.createElement("span");
    c.textContent = characters[i];
    el.appendChild(c);
    await sleep(50);
  }

  index += 1;
  if (index >= lines.length) index = 0;

  if (index % 10 === 0) {
    setTimeout(() => {
      app.innerHTML = "";
      showLineCharacters();
    }, lineTime);
  } else {
    setTimeout(showLineCharacters, lineTime);
  }
}

async function main() {
  // let response = await fetch("./all_births_and_deaths.txt");
  let response = await fetch("../births_and_deaths.txt");
  lines = await response.text();
  lines = lines.split("\n");
  // showLine();
  showLineCharacters();
}

main();
