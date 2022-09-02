const urlParams = new URLSearchParams(window.location.search);
let transition = urlParams.get("transition") || 10000; //5000
let restingTime = urlParams.get("rest") || 2000; // 2000
const direction = urlParams.get("direction") || "up";
const paddingH = urlParams.get("paddh") || 2;
const paddingV = urlParams.get("paddv") || 10;

transition = +transition;
restingTime = +restingTime;

const animation = direction == "down" ? "slide-down" : "slide-up";

// the exxon valdex
const startTime = new Date(Date.UTC(1989, 3, 24, 0, 0, 0));
const startSeconds = Math.floor(startTime.getTime() / 1000);
let totalTime;

let lines = [];
let index = 0;
let container = document.getElementById("app");
let timeout;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function slideShow() {
  clearTimeout(timeout);

  let line = lines[index];
  const el = document.createElement("div");
  el.classList.add("content");
  el.style.padding = `${paddingV}vh ${paddingH}vh`;
  // line = line.replace("It produced", "<br><br>It produced");
  el.innerHTML = `<p>${index + 1} of ${lines.length}</p>${line}`;
  // el.textContent = `${line}`;
  el.style.animation = `${animation}-in ${transition}ms linear forwards`;
  container.prepend(el);
  textFit(el, { maxFontSize: 1000, reProcess: true });

  const els = container.querySelectorAll("div");
  if (els.length > 1) {
    els[1].style.animation = `${animation}-out ${transition}ms linear forwards`;
    setTimeout(() => {
      els[1].remove();
    }, transition);
  }

  index += 1;
  if (index >= lines.length) index = 0;

  timeout = setTimeout(slideShow, restingTime + transition);
}

async function main() {
  let response = await fetch("births_and_deaths.txt");
  lines = await response.text();
  lines = lines.split("\n");
  const slideTime = (transition + restingTime) / 1000;
  totalTime = slideTime * lines.length;
  const currentSeconds = Math.floor(new Date().getTime() / 1000);
  index = Math.floor((currentSeconds - startSeconds) / slideTime) % lines.length;
  if (index >= lines.length) index = 0;
  const currentTime = new Date().getTime();
  const nextSlide = new Date(
    Math.ceil((currentTime - startTime.getTime()) / (transition + restingTime)) *
      (transition + restingTime) +
      startTime.getTime()
  );
  const delay = nextSlide - currentTime;
  setTimeout(slideShow, delay);
  // slideShow();
}

window.addEventListener("resize", () => {
  const els = container.querySelectorAll("div");
  els.forEach(el => {
    textFit(el, { maxFontSize: 1000, reProcess: true });
  });
});

main();
