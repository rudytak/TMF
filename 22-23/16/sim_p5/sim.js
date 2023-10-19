const pi = Math.PI;
const atm = 101325; // Pa
const absZ = 273.15; // K
const N_A = 6.0221408e23;
const k_B = 1.380649e-23;
const R = 8.31446261815324;

let params = {
  r: 20.63e-3 / 2, // [m] test tube radius
  l: 0.15, // [m] test tube length
  p_0: 1 * atm, // [Pa] ambient pressure
  p_drive: 0.1 * atm, // [Pa] amplitude of the driving pressure
  T_drive: 1 / 2000, // [s] period of the driving oscillation
  tau: 1e-6, // [s] simulation time step
  runtime: 0.01, // [s] duration od the simulation
  layers: 250, // [-] number of layers

  heater_a: 0.0001,
  heater_temp: 1100 + absZ,
  cooler_a: 0.000015,
  cooler_temp: 0 + absZ,
};

// LOAD PARAMATERS
let r = params.r;
let l = params.l; // 15 cm

let p_0 = params.p_0;
let p_amp = params.p_drive;
let period_drive = params.T_drive;

let layerCount = params.layers;
let run_time = params.runtime;
let tau = params.tau;

// CALCULATE DERIVED VARIABLES
let S = pi * r * r;
let omega_drive = (2 * Math.PI) / period_drive;
let Q_h = 0;
let Q_c = 0;
let sim_t = 0;
let prevD = 0;

// DEFINE CLASSES
class TempArea {
  constructor(start, end, temp, transferCoeff, type) {
    // heater or cooler or none
    this.start = start;
    this.end = end;
    this.temp = temp;
    this.alph = transferCoeff;

    this.type = type;
  }

  overlap(layer, lx) {
    let start = max(lx, this.start);
    let end = min(lx + layer.d, this.end);
    let d = end - start;
    if (d < 0) {
      return 0;
    }
    return d;
  }
}

class Layer {
  constructor(p, V, T) {
    this.p = p; // Pa
    this.V = V; // m**3
    this.T = T; // K

    // GAS - AIR
    this.kappa = 5 / 3;
    this.molarM = 28.97e-3; // kg/mol
    this.start_density = 1.225; // kg/m**3
    this.c_p = 1.005;

    // CONSTS
    this.pVkappa_const = p * V ** this.kappa;
    this.m = V * this.start_density; // kg
    this.n = this.m / this.molarM;
  }

  get density() {
    return this.m / this.V;
  }

  get d() {
    return this.V / S;
  }

  set_p_adiabat(new_p) {
    // this.V = Math.pow(this.pVkappa_const / new_p, 1 / this.kappa);
    this.T = this.T * Math.pow(new_p / this.p, (this.kappa - 1) / this.kappa);
    this.V = (this.n * R * this.T) / new_p;
    this.p = new_p;
  }

  accept_temp(h, pos, time) {
    let affected_area = h.overlap(this, pos);
    if (affected_area == 0) return;

    this.T =
      this.T +
      ((h.temp - this.T) * time * h.alph * affected_area) /
        this.d /
        (this.m * this.c_p);

    // console.log(Q * ((h.type == "cooler")?-1:1))
    switch (h.type) {
      case "heater":
        Q_h += ((h.temp - this.T) * time * h.alph * affected_area) / this.d;
        break;
      case "cooler":
        Q_c -= ((h.temp - this.T) * time * h.alph * affected_area) / this.d;
        break;
    }

    // pV = nRT
    this.V = (this.n * R * this.T) / this.p;
  }
}

// PREAPARE LAYERS
layers = [];
for (var i = 0; i < layerCount; i++) {
  layers.push(new Layer(p_0, (S * l) / layerCount, 20 + absZ));
}

// PREPARE HEATERS
let heaters = [
  new TempArea(0.025, 0.0475, params.heater_temp, params.heater_a, "heater"),
  new TempArea(0.0525, 0.075, params.cooler_temp, params.cooler_a, "cooler"),
  // new TempArea(0.0, 0.15, 20 + absZ, 0.001, "cooler"),
];

function iter() {
  let p_glob = p_0 + Math.sin(omega_drive * sim_t) * p_amp;
  for (let l of layers) {
    l.set_p_adiabat(p_glob);
  }

  let totD = 0;
  for (let l of layers) {
    for (let h of heaters) {
      l.accept_temp(h, totD, tau);
    }
    totD += l.d;
  }
  prevD = totD;

  old_t = sim_t;
  sim_t += tau;

  return [
    //["P/W", old_t, (p_glob - p_0) * S * totD / tau],
    //["p/Pa", old_t, p_glob],
    ["Qh/J", old_t, Q_h],
    ["Qc/J", old_t, Q_c],
  ];
}
