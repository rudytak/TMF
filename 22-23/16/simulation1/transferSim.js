const c_p = 1000; // J/kg*K
const λ = 0.025; // W/m*K
const ρ = 1.2; // kg/m**2
const d = 1 / 1000; // 1 mm

let T_predict = (d ** 2 * c_p * ρ) / λ;

let divs = 1000;
let k = 1 / 5;

let dt = 0.0000000001;
let totT = 0;

let temps = Array(divs).fill(0);
temps[0] = 100;

console.log("start");

while (temps[divs - 1] < k * temps[0]) {
// for(var j = 0; j < 5; j++){
  temps[0] = 100;

  let deltas = Array(divs - 1).fill(0);

  for (var i = 0; i < deltas.length; i++) {
    deltas[i] =
      (Math.abs(temps[i] - temps[i + 1]) * dt * λ) /
      (c_p * ρ * (d / divs) ** 2);
  }

  for (var i = 0; i < deltas.length; i++) {
    temps[i + 1] += deltas[i];
    temps[i] -= deltas[i];
  }
//   console.log(deltas)

  totT += dt;
}

console.log(1 / totT, 1 / T_predict);
