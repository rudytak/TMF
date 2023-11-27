const { v3, v } = require("../vec.js");

// Constants
const PI = Math.PI;

// spinner
let r_0 = 0.035; // effective radius of the spinners

// magnetism
let μ_0 = PI * 4e-7; // permeability of vacuum [H/m]
let B_r_mag = 1.4; // magnitude residual flux densitty [T]
let V = 0.005 ** 3; // volume of magnet [m^3] (5mm cubed)
let m_mag = (1 / μ_0) * B_r_mag * V; // magnitude of magnetic moment [A*m^2]

// rotation
let α = 0.868;
let γ = 0.00068;
// let I_0 = (1 / 2) * 0.06 * 0.03; // guessed moment of inertia
// let I_0 = 0.000045; // stolen from here https://www.wired.com/2017/05/physics-of-a-fidget-spinner/
// let I_0 = 0.00178; // measured moment of inertia INCORRECT??
let I_0 = 4.525e-5; // measured

// spinner
class spinner {
  constructor(
    center,
    phi0,
    ω0,
    magnet_count = 3,
    _r = r_0,
    _I = I_0,
    _m_mag = m_mag
  ) {
    this.S = center;
    this.phi = phi0; // angle
    this.ω = ω0; // angular velocity
    this.I = _I; // moment of inertia
    this.r = _r; // 4 cm
    this.n = magnet_count; // 3
    this.m_mag = _m_mag;
  }

  P(i) {
    return v(
      this.S.x + this.r * Math.cos(this.phi + (2 * PI * i) / this.n),
      this.S.y + this.r * Math.sin(this.phi + (2 * PI * i) / this.n),
      this.S.z
    );
  }

  draw() {
    stroke("yellow");
    strokeWeight(0.02);
    point(this.S.x, this.S.y);
    stroke("white");
    strokeWeight(0.01);
    for (let j = 0; j < this.n; j++) {
      let _p = this.P(j);
      point(_p.x, _p.y);
    }
  }

  m(i) {
    // return this.P(i).sub(this.S).unit().mult(m_mag);
    return v(0, 0, this.m_mag);
    // return v3.cross(v(0, 0, 1), this.P(i).sub(this.S)).unit().mult(m_mag);
  }
}

function F(r, m1, m2) {
  let p1 = m2.mult(v3.dot(m1, r));
  let p2 = m1.mult(v3.dot(m2, r));
  let p3 = r.mult(v3.dot(m1, m2));
  let p4 = r.mult((-5 * v3.dot(m1, r) * v3.dot(m2, r)) / r.mag() ** 2);

  return p1
    .add(p2)
    .add(p3)
    .add(p4)
    .mult((3 * μ_0) / (4 * PI * r.mag() ** 5));
}

function B(r, m) {
  let ru = r.unit();
  return ru
    .mult(3 * v3.dot(ru, m))
    .sub(m)
    .mult(μ_0 / (4 * PI * r.mag() ** 3));
}

function dω(m_ex, P_ex, s) {
  let τ_tot = v(0, 0, 0);

  for (let j = 0; j < s.n; j++) {
    let m_in = s.m(j);
    let P_in = s.P(j);

    // magnetic force interactions
    let r = P_ex.sub(P_in);
    let f = F(r, m_in, m_ex);
    let force_arm = P_in.sub(s.S);
    let τ_F = v3.cross(f, force_arm);

    // magnetic moment interactions
    let r_neg = r.mult(-1);
    let B_ex = B(r_neg, m_ex);
    let τ_mag = v3.cross(m_in, B_ex);

    τ_tot = τ_tot.add(τ_mag);
    τ_tot = τ_tot.add(τ_F);
  }

  τ_tot = τ_tot.mult(dt / s.I);

  return τ_tot;
}

// spinner creation
let s1 = new spinner(v(0, 0, 0), 0, 100);
let s2 = new spinner(v(800, 0, 0), 0, 10);

// rozměry velký magent
// 47x22x9.5 mm**3

// hmotnost malý magnet
// 0.92(2) g

// sim iteration
function step() {
  for (let j = 0; j < s1.n; j++) {
    let m_ex = s1.m(j);
    let P_ex = s1.P(j);
    s2.ω += dω(m_ex, P_ex, s2).z;
  }

  for (let j = 0; j < s2.n; j++) {
    let m_ex = s2.m(j);
    let P_ex = s2.P(j);
    s1.ω += dω(m_ex, P_ex, s1).z;
  }

  s2.ω = 10;

  // omega damping
  // s1.ω += dt * (-α - γ * s1.ω ** 2);
  // s2.ω += dt * (-α - γ * s2.ω ** 2);

  let damp_1 = dt * (-α - γ * s1.ω ** 2) * Math.sign(s1.ω);
  let damp_2 = dt * (-α - γ * s2.ω ** 2) * Math.sign(s2.ω)

  if (Math.abs(s1.ω) > 2 * Math.abs(damp_1)) {
    s1.ω += damp_1;
  }
  // if (Math.abs(s2.ω) > 2 * Math.abs(damp_2)) {
  //   s2.ω += damp_2;
  // }

  // rotation
  s1.phi += s1.ω * dt;
  s2.phi += s2.ω * dt;
}
// TODO - RK4

let dt = 1e-3; // 1 ms
let run_time = 25;
let save_freq = Math.ceil(1e-3 / dt + 1) - 1;
let out_path = `out_eu_old.csv`;

const fs = require("fs");
fs.writeFileSync(out_path, "t, ω_1, ω_2 \n");

// running sim
let frame = 0;
for (var t = 0; t < run_time; t += dt) {
  if (frame % save_freq == 0) {
    fs.appendFileSync(out_path, `${t}, ${s1.ω}, ${s2.ω}\n`);
  }

  step();

  frame++;
}

// FFT

// let data = fs.readFileSync(out_path, 'utf8')
// let dataArray = data.split(/\r?\n/).map(r=>r.split(", ").map(x=>parseFloat(x))).slice(1, -2);  //Be careful if you are in a \r\n world...

// var signal = dataArray.map(r=>r[1])
// const FFT = require('fft.js');
// const f = new FFT(4096);

// const out = f.createComplexArray();
// f.realTransform(out, signal);

// console.log(out)

// // console.log(both);
