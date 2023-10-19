const fs = require("fs");

// Ignoring air resistance, deformation is instant, ignoring hysterisis

let maxH = 1;
let height_inc = 0.01;
let output_lines = Array(5).fill("");
output_lines[0] = "Avg [cm]"
output_lines[1] = "Quart [cm]"
output_lines[2] = "Median [cm]"
output_lines[3] = "3Quart [cm]"
output_lines[4] = "Max [cm]"
let collision_count = 10000;

for (let j = 0.1; j <= 0.9; j += 0.1) {
  // σηδωνρ
  pi = Math.PI;
  g = 9.81;
  sgn = Math.sign;

  // Time simulation variables
  τ = 2.5e-9;
  t = 0;
  t_off = 0;

  // Ferit
  _k = 0.2;

  l = 15e-2; // m
  f_R = 15.3e3; // Hz
  f_L = f_R / 2; // Hz
  ω_R = 2 * pi * f_R; // rad/s
  ω_L = 2 * pi * f_L; // rad/s
  σ_max = 40e6; // Pa
  ρ_fer = 5e3; // kg/m^3
  y_max = (_k * pi * σ_max) / (l * ρ_fer * ω_R ** 2); // m
  fer_t = () => t + t_off;
  y_fer = () => y_max * F(Math.cos(ω_R * fer_t()));

  // Magnetosctriction behaviour parameter
  v_fer = () => -y_max * ω_R * Math.sin(ω_R * fer_t());
  F = (x) => x;

  // Kulička
  r = 2e-3; // m
  ρ_steel = 7750; // kg/m^3
  m = ((ρ_steel * 4) / 3) * pi * r * r * r; // kg
  y_0 = 0;
  h = 0.01;
  E = m * g * h;
  v_0 = Math.sqrt(2 * g * h);
  y_ball = () => y_0 + v_0 * t - 0.5 * g * t * t;
  v_ball = () => v_0 - g * t;
  e = j;

  // Statistic
  h_0 = h;
  close_region_count = 0;

  // Simulation
  // Starting off by throwing the ball in the air to height h+y_0 from height y_0

  let heights = [];
  let height_categories = 10;

  for (var i = 0; i < collision_count; i) {
    // calcuale and jump by t_min to the next possible collision region
    t_min = (v_0 + Math.sqrt(v_0 * v_0 + 2 * g * (y_0 - y_max))) / g;
    t += t_min - τ; // minus one cycle for some extra leeway

    function await_collision() {
      log = "";
      // perform close simulation steps until collision
      while (y_fer() <= y_ball()) {
        t += τ;
        // log += `${fer_t()}, ${y_fer()}, ${y_ball()} \n`
      }

      // Recalculate ball velocity
      y_0 = y_fer();
      v_f = v_fer();
      v_k = v_ball();

      // only add the velocity of the ferite back if it moving up
      v_0 = e * (v_f - v_k) + (v_f > 0 ? v_f : 0);

      // reset times
      t_off += t;
      t = 0;

      // Update energy and max height
      E = (1 / 2) * m * v_0 * v_0;
      h = (v_0 * v_0) / (2 * g);

      // add to collision counter
      heights.push(h);
      i++;
      return log;
    }

    log = await_collision();
    // perform close simulation step until the ball fly's out of the close region
    while (v_0 * v_0 + 2 * g * (y_0 - y_max) < 0) {
      log += await_collision();
      close_region_count++;

      // fs.writeFileSync(
      //   `./close_region_logs/checkLog${close_region_count}.csv`,
      //   "t, y_fer, y_ball, \n" + log
      // )
    }
  }

  console.log("EXPORTING");

  output_lines[0] += `, ${heights.reduce((a,b)=>a+b)/heights.length}`;
  output_lines[1] += `, ${heights.sort((a,b)=>a<b)[Math.floor(heights.length * 1/4)]}`;
  output_lines[2] += `, ${heights.sort((a,b)=>a<b)[Math.floor(heights.length * 1/2)]}`;
  output_lines[3] += `, ${heights.sort((a,b)=>a<b)[Math.floor(heights.length * 3/4)]}`;
  output_lines[4] += `, ${Math.max(...heights)}`;
}

output_data = "Total Collision Count, Time increment tau[s] \n";
output_data += `${collision_count}, ${τ} \n`;

output_data += "\n h, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, e \n";

// HISTOGRAMS
for (var i = 0; i < 5; i ++) {
  output_data += output_lines[i] + `\n`;
}

fs.writeFileSync(`output_ee.csv`, output_data);
