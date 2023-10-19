// vectors
class v3 {
  constructor(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }

  mult(k) {
    return v(this.x * k, this.y * k, this.z * k);
  }
  unit() {
    return this.mult(1 / this.mag());
  }
  mag() {
    return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
  }

  add(v2) {
    return v3.add(this, v2);
  }

  sub(v2) {
    return v3.sub(this, v2);
  }

  static add(v1, v2) {
    return v(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z);
  }

  static add_many(v_arr) {
    return v(
      v_arr.reduce((c, v) => c + v.x, 0),
      v_arr.reduce((c, v) => c + v.y, 0),
      v_arr.reduce((c, v) => c + v.z, 0)
    );
  }

  static sub(v1, v2) {
    return v(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);
  }

  static dot(v1, v2) {
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
  }

  static cross(v1, v2) {
    return new v(
      v1.y * v2.z - v1.z * v2.y,
      v1.x * v2.z - v1.z * v2.x,
      v1.x * v2.y - v1.y * v2.x
    );
  }
}
v3.prototype.toString = function () {
  return { x: this.x, y: this.y, z: this.z }.toString();
};
function v(x, y, z = 0) {
  return new v3(x, y, z);
}

// Constants
const PI = Math.PI;
let dt = 1e-2; // 1 ms

// spinner
let r_0 = 0.04; // effective radius of the spinners

// magnetism
let μ_0 = PI * 4e-7; // permeability of vacuum [H/m]
let B_r_mag = 1.23; // magnitude residual flux density [T]
let V = 0.005 ** 3; // volume of magnet [m^3] (5mm cubed)
let m_mag = (1 / μ_0) * B_r_mag * V; // magnitude of magnetic moment [A*m^2]

// rotation
let λ = 1 / 100; // approximate decay rate - TODO
let I_0 = (1 / 2) * 0.06 * 0.03; // appproximate moment of inertia - TODO

// spinner
class spinner {
  constructor(center, phi0, ω0, magnet_count = 3) {
    this.S = center;
    this.phi = phi0; // angle
    this.ω = ω0; // angular velocity
    this.I = I_0; // moment of inertia (cca)
    this.r = r_0; // 4 cm
    this.n = magnet_count; // 3
  }

  P(i) {
    return v(
      this.S.x + this.r * Math.cos(this.phi + (2 * PI * i) / this.n),
      this.S.y + this.r * Math.sin(this.phi + (2 * PI * i) / this.n),
      this.S.z
    );
  }

  m(i) {
    // return this.P(i).sub(this.S).unit().mult(m_mag);
    // return v(0, 0, m_mag);
    return v3.cross(v(0, 0, 1), this.P(i).sub(this.S)).unit().mult(m_mag);
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
    .mult(3 * v3.dot(m, ru))
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
let s1 = new spinner(v(0, 0, 0), 0, 0);
let s2 = new spinner(v(0.1, 0, 0), PI * 0.99, 0);

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

  // rotation
  s1.phi += s1.ω * dt;
  s2.phi += s2.ω * dt;

  // omega damping
  s1.ω *= Math.exp(-λ * dt);
  s2.ω *= Math.exp(-λ * dt);
}

// TODO - RK4

const fs = require("fs");
fs.writeFileSync(`out${dt}.csv`, "t, ω_1, EK_1, ω_2, EK_2 \n");

// running sim
for (var t = 0; t < 10; t += dt) {
  step();

  fs.appendFileSync(`out${dt}.csv`, `${t}, ${s1.ω}, ${1/2 * s1.ω**2}, ${s2.ω}, ${1/2 * s2.ω**2} \n`);

}