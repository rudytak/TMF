const fs = require("fs");
const { v3, v } = require("./vec.js");

// ΑαΔδΗηΒβΕεΘθΓγΖζΙιΚκΝνΠπΛλΞξΡρΜμΟοΣςΤτΧχσΥυΨψΦφΩωϜϝ

// spinner definition
class spinner {
  constructor(
    center,
    φ0,
    ω0,
    magnet_count = 3,
    _r,
    _I,
    _m_0,
    magnet_orientation,
    α,
    β,
    γ,
    constant_ω
  ) {
    this.S = center;
    this.φ0 = φ0; // angle
    this.φ = φ0; // angle
    this.ω0 = ω0; // angular velocity
    this.ω = ω0; // angular velocity
    this.I = _I; // moment of inertia
    this.r = _r; // 4 cm
    this.n = magnet_count; // 3
    this.m_0 = _m_0;
    this.mag_orientation = magnet_orientation;

    this.α = α;
    this.β = β;
    this.γ = γ;
    this.constant_ω = constant_ω;
  }

  P(i) {
    return v(
      this.S.x + this.r * Math.cos(this.φ + (2 * Math.PI * i) / this.n),
      this.S.y + this.r * Math.sin(this.φ + (2 * Math.PI * i) / this.n),
      this.S.z
    );
  }

  m(i) {
    switch (this.mag_orientation) {
      case "tangent":
        return v3
          .cross(v(0, 0, 1), this.P(i).sub(this.S))
          .unit()
          .mult(this.m_0);
        break;

      case "radial":
        return this.P(i).sub(this.S).unit().mult(this.m_0);
        break;

      default:
      case "vertical":
        return v(0, 0, this.m_0);
        break;
    }
  }

  copy() {
    let ns = new spinner(
      this.S,
      this.φ,
      this.ω,
      this.n,
      this.r,
      this.I,
      this.m_0,
      this.mag_orientation,
      this.α,
      this.β,
      this.γ,
      this.constant_ω
    );
    ns.ω_0 = this.ω_0;

    return ns;
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
}

// table as per:
// https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods#Explicit_Runge%E2%80%93Kutta_methods
class RK_matrix {
  static epsilon = 0.000000001;
  static get Euler() {
    return new RK_matrix([], [1], [0]);
  }
  static get Midpoint() {
    return RK_matrix.Second_Order(1 / 2);
  }
  static get Heun2() {
    return RK_matrix.Second_Order(1);
  }
  static get Ralston2() {
    return RK_matrix.Second_Order(2 / 3);
  }
  static get Ralston4() {
    return new RK_matrix(
      [[0.4], [0.29697761, 0.15875964], [0.2181004, -3.05096516, 3.83286476]],
      [0.17476028, -0.55148066, 1.2055356, 0.17118478],
      [0, 0.4, 0.45573725, 1]
    );
  }
  static get RK_3_8() {
    return new RK_matrix(
      [[1 / 3], [-1 / 3, 1], [1, -1, 1]],
      [1 / 8, 3 / 8, 3 / 8, 1 / 8],
      [0, 1 / 3, 2 / 3, 1]
    );
  }
  static get RK4() {
    return new RK_matrix(
      [[1 / 2], [0, 1 / 2], [0, 0, 1]],
      [1 / 6, 1 / 3, 1 / 3, 1 / 6],
      [0, 1 / 2, 1 / 2, 1]
    );
  }

  static Second_Order(alp) {
    // https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods#Second-order_methods_with_two_stages

    return new RK_matrix([[alp]], [1 - 1 / (2 * alp), 1 / (2 * alp)], [0, alp]);
  }

  constructor(a, b, c) {
    this.a = a;
    this.b = b;
    this.c = c;

    if (Math.abs(this.b.reduce((i, j) => i + j) - 1) > RK_matrix.epsilon) {
      throw new Error(`The RK matrix "b" components do not sum up to 1.`);
    }

    if (this.c[0] != 0) {
      throw new Error(`The first RK matrix "c" component is not equal to 0.`);
    }

    for (let i = 0; i < a.length; i++) {
      if (a[i].length <= i) {
        throw new Error(
          `The row number ${
            i + 1
          } in the RK matrix "a" components is not sufficiently long.`
        );
      }
    }
  }
}

// in this case th input are all of the spinner positions
// and the outputs are their new angular velocities
class omega_state {
  constructor(dt, spinners, auto_calc = true) {
    this.dt = dt;
    this.spinners = spinners;

    this.spinners.forEach((s) => {
      s.φ += this.dt * s.ω;
    });

    this.ang_accelerations = [];

    if (auto_calc) {
      this.calculate();
    }
  }

  static F(r, m1, m2) {
    let p1 = m2.mult(v3.dot(m1, r));
    let p2 = m1.mult(v3.dot(m2, r));
    let p3 = r.mult(v3.dot(m1, m2));
    let p4 = r.mult((-5 * v3.dot(m1, r) * v3.dot(m2, r)) / r.mag() ** 2);

    return p1
      .add(p2)
      .add(p3)
      .add(p4)
      .mult((3 * sim_instance.constants.μ_0) / (4 * Math.PI * r.mag() ** 5));
  }

  static B(r, m) {
    let ru = r.unit();
    return ru
      .mult(3 * v3.dot(ru, m))
      .sub(m)
      .mult(sim_instance.constants.μ_0 / (4 * Math.PI * r.mag() ** 3));
  }

  static τ(m_ex, P_ex, s) {
    let τ_tot = v(0, 0, 0);

    for (let j = 0; j < s.n; j++) {
      let m_in = s.m(j);
      let P_in = s.P(j);

      // magnetic force interactions
      let r = P_ex.sub(P_in);
      let f = omega_state.F(r, m_in, m_ex);
      let force_arm = P_in.sub(s.S);
      let τ_F = v3.cross(f, force_arm);

      // magnetic moment interactions
      let r_neg = r.mult(-1);
      let B_ex = omega_state.B(r_neg, m_ex);
      let τ_mag = v3.cross(m_in, B_ex);

      τ_tot = τ_tot.add(τ_mag);
      τ_tot = τ_tot.add(τ_F);
    }

    τ_tot = τ_tot.mult(1 / s.I);

    return τ_tot;
  }

  calculate() {
    let torques = this.spinners.map((s) => 0);

    for (let i = 0; i < this.spinners.length; i++) {
      // select spinner 1
      let s1 = this.spinners[i];

      for (let j = 0; j < this.spinners.length; j++) {
        // select spinner 2
        let s2 = this.spinners[j];

        //make sure we are talking about distinc spinners

        if (i != j) {
          if (s2.constant_ω) {
            torques[j] = 0;
          } else {
            for (let k = 0; k < s1.n; k++) {
              // go through each magnet on s1 and calculates it's effect on s2
              let m_ex = s1.m(k);
              let P_ex = s1.P(k);

              // the change in angular velocity done to s2
              torques[j] += omega_state.τ(m_ex, P_ex, s2).z;
            }
          }
        }
      }
    }

    for (let i = 0; i < this.spinners.length; i++) {
      let s = this.spinners[i];

      // if the spinner should be kept at a constant omega, keep it at that
      if (s.constant_ω) {
        torques[i] = 0;
      } else {
        // get the value of the spinners new angular velocity
        let new_sω = s.ω + torques[i];

        // omega damping
        // s.ω += dt * (-α - β * s.ω - γ * s.ω ** 2);
        // damping acceleration
        let damp =
          (-s.α - s.β * new_sω - s.γ * new_sω ** 2) * Math.sign(new_sω);

        // perform dampening only when  the omega is not practically 0
        if (Math.abs(new_sω) > 2 * Math.abs(damp) * this.dt) {
          torques[i] += damp;
        }
      }
    }

    // save the output
    this.ang_accelerations = torques;
  }

  static sum_omeg_states(states, weights = []) {
    let sum = states[0].ang_accelerations.map((o) => 0);

    states.forEach((state, s_id) => {
      state.ang_accelerations.forEach((d_omeg, id) => {
        sum[id] += d_omeg * weights[s_id];
      });
    });

    let out_state = new omega_state(0, [], false);
    out_state.ang_accelerations = sum;
    return out_state;
  }

  static apply_omeg_to_spinners(dt, spinners, state, including_ang = true) {
    // rotation
    spinners.forEach((s, id) => {
      s.ω += state.ang_accelerations[id] * dt;
      if (including_ang) {
        s.φ += s.ω * dt;
      }
    });

    return spinners;
  }
}

class phi_state {
  constructor(dt, spinners, auto_calc = true) {
    this.dt = dt;
    this.spinners = spinners;

    this.spinners.forEach((s) => {
      s.φ += this.dt * s.ω;
    });

    this.ωs = [];

    if (auto_calc) {
      this.calculate();
    }
  }

  calculate() {
    // save the output
    this.ωs = this.spinners.map((s) => s.ω);
  }

  static sum_φ_states(states, weights) {
    let sum = states[0].ωs.map((p) => 0);

    states.forEach((state, s_id) => {
      state.ωs.forEach((ω, id) => {
        sum[id] += ω * weights[s_id];
      });
    });

    let out_state = new phi_state(0, [], false);
    out_state.ωs = sum;
    return out_state;
  }

  static apply_φ_to_spinners(dt, spinners, state) {
    spinners.forEach((s, id) => {
      // euler-like omega => φ calc
      s.φ += state.ωs[id] * dt;
    });

    return spinners;
  }
}

class sim_instance {
  static constants = {
    PI: Math.PI,
    μ_0: Math.PI * 4e-7,
  };

  constructor(
    sim_run_overrides = {},
    RKmatrix = RK_matrix.RK4,
    default_overrides = {}
  ) {
    this.sim_run_params = {
      dt: 1e-3, // 1 ms
      end_time: 1,
      start_time: 0,
      get save_freq() {
        return Math.ceil(1e-3 / this.dt + 1) - 1;
      },
      out_path: `out.csv`,
      exports: ["s[0].ω", "s[0].φ"],

      // apply the overrides
      ...sim_run_overrides,
    };

    this.defaults = {
      // these defaults don't really have a reason to be changed
      r: 0.0359, // effective radius of the spinners
      B_r: 1.1049, // magnitude residual flux densitty [T]
      V: 0.005 ** 3, // volume of magnet [m^3] (5mm cubed)
      I: 4.8e-5, // measured
      get m_0() {
        // magnitude of magnetic moment [A*m^2]
        return (1 / sim_instance.constants.μ_0) * this.B_r * this.V;
      },
      magnet_count: 3,
      magnet_orientation: "vertical", // "vertical", "radial", "tangent"

      // these defaults can be overriden
      α: 0.868,
      β: 0,
      γ: 0.00068,

      // apply the overrides
      ...default_overrides,
    };

    // define the numerical method matrix
    this.RKmatrix = RKmatrix;

    // array of all the spinners in the scene
    this.spinner_params = [];
    this.spinners = [];

    this.t = 0;
    this.frame = 0;
  }

  reset_spinners() {
    this.spinners = [];
    // re-instantiate the spinner instances
    for (let params of this.spinner_params) {
      this.spinners.push(new spinner(...params));
    }
  }

  add_spinner(
    S,
    φ_0,
    ω_0,

    constant_ω = false,
    α = this.defaults.α,
    β = this.defaults.β,
    γ = this.defaults.γ,
    magnet_orientation = this.defaults.magnet_orientation,

    magnet_count = this.defaults.magnet_count,
    r = this.defaults.r,
    I = this.defaults.I,
    m_0 = this.defaults.m_0
  ) {
    this.spinner_params.push([
      S,
      φ_0,
      ω_0,
      magnet_count,
      r,
      I,
      m_0,
      magnet_orientation,
      α,
      β,
      γ,
      constant_ω,
    ]);
  }

  remove_spinner(i) {
    this.spinner_params.splice(i, 1);
    this.reset_spinners();
  }

  calc_omegas(dt) {
    // RK calculation
    let k = [new omega_state(0, this.spinners)];
    for (var i = 1; i < this.RKmatrix.b.length; i++) {
      let c = this.RKmatrix.c[i];
      let as = this.RKmatrix.a[i - 1];

      let spins = omega_state.apply_omeg_to_spinners(
        c * dt,
        this.spinners.map((s) => s.copy()), // make a copy of the current spinner objects
        omega_state.sum_omeg_states(k, as)
      );
      let k_i = new omega_state(0, spins);
      k.push(k_i);
    }

    return omega_state.apply_omeg_to_spinners(
      dt,
      this.spinners.map((s) => s.copy()),
      omega_state.sum_omeg_states(k, this.RKmatrix.b),
      false
    );
  }

  step() {
    let dt = this.sim_run_params.dt;

    // RK calculation
    let k = [new phi_state(0, this.spinners)];
    for (var i = 1; i < this.RKmatrix.b.length; i++) {
      let c = this.RKmatrix.c[i];
      let as = this.RKmatrix.a[i - 1];

      let omeg_spins = this.calc_omegas(c * dt);
      let spins = phi_state.apply_φ_to_spinners(
        c * dt,
        omeg_spins, // make a copy of the projected spinner objects
        phi_state.sum_φ_states(k, as)
      );
      let k_i = new phi_state(0, spins);
      k.push(k_i);
    }

    // save the new calculated step
    this.spinners = phi_state.apply_φ_to_spinners(
      dt,
      this.calc_omegas(dt).map((s) => s.copy()),
      phi_state.sum_φ_states(k, this.RKmatrix.b)
    );
  }

  run() {
    // init run
    this.reset_spinners();
    this.frame = 0;
    fs.writeFileSync(
      this.sim_run_params.out_path,
      `t, ${this.sim_run_params.exports.join(", ")} \n`
    );

    for (
      // time variable
      this.t = this.sim_run_params.start_time;
      this.t < this.sim_run_params.end_time;
      this.t += this.sim_run_params.dt
    ) {
      this.step();

      // save the simulation state every save_freq frames
      if (this.frame % this.sim_run_params.save_freq == 0) {
        let s = this.spinners;
        fs.appendFileSync(
          this.sim_run_params.out_path,
          `${t}, ${this.sim_run_params.exports
            .map((ex) => eval(ex))
            .join(", ")} \n`
        );
      }
      this.frame++;
    }

    console.log(`${this.sim_run_params.out_path} simulation finished`);
  }

  prerunWeb() {
    // init run
    this.reset_spinners();
    this.frame = 0;
    fs.writeFileSync(
      this.sim_run_params.out_path,
      `t, ${this.sim_run_params.exports.join(", ")} \n`
    );
    this.t = this.sim_run_params.start_time;
  }

  runWebFrame() {
    this.step();

    for(var s of this.spinners){
      s.draw();
    }

    // save the simulation state every save_freq frames
    if (this.frame % this.sim_run_params.save_freq == 0) {
      let s = this.spinners;
      fs.appendFileSync(
        this.sim_run_params.out_path,
        `${t}, ${this.sim_run_params.exports
          .map((ex) => eval(ex))
          .join(", ")} \n`
      );
    }
    this.frame++;
    this.t += this.sim_run_params.dt;

    return this.t < this.sim_run_params.end_time;
  }
}

module.exports = {
  sim_instance,
  RK_matrix,
};
