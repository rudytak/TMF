const fs = require("fs");

// Ignoring air resistance, deformation is instant, ignoring hysterisis

// σηδωνρ
pi = Math.PI;
g = 9.81;
sgn = Math.sign;

// Time simulation variables
τ = 2.5e-9;
t = 0;
t_off = 0;

// Ferit
l = 15e-2; // m
f_R = 15.3e3; // Hz
f_L = f_R / 2; // Hz
ω_R = 2 * pi * f_R; // rad/s
ω_L = 2 * pi * f_L; // rad/s
σ_max = 40e6; // Pa
ρ_fer = 5e3; // kg/m^3
y_max = σ_max / (l * ρ_fer * ω_R ** 2); // m
fer_t = () => t + t_off;
y_fer = () => y_max * F(Math.cos(ω_L * fer_t()));

// Magnetosctriction behaviour parameter
v_fer = () =>
  -0.5 * y_max * ω_L * Math.tan(ω_L * fer_t()) * Math.sqrt(Math.abs(Math.cos(ω_L * fer_t())));
F = (x) => Math.sqrt(Math.abs(x));

// Kulička
r = 2e-3; // m
ρ_steel = 7750; // kg/m^3
m = ((ρ_steel * 4) / 3) * pi * r * r * r; // kg
y_0 = 0;
h = 0.1;
E = m * g * h;
v_0 = Math.sqrt(2 * g * h);
y_ball = () => y_0 + v_0 * t - 0.5 * g * t * t;
v_ball = () => v_0 - g * t;
e = 0.715;

// Statistic
h_0 = h
close_region_count = 0;

// Simulation
// Starting off by throwing the ball in the air to height h+y_0 from height y_0

let collision_count = 1000000;
let heights = [];
let height_categories = 1000;

for (var i = 0; i < collision_count; i) {
  // calcuale and jump by t_min to the next possible collision region
  t_min = (v_0 + Math.sqrt(v_0 * v_0 + 2 * g * (y_0 - y_max))) / g;
  t += t_min - τ; // minus one cycle for some extra leeway

  function await_collision() {
    log = "";
    // perform close simulation steps until collision
    while (y_fer() <= y_ball()) {
      t += τ;
      log += `${fer_t()}, ${y_fer()}, ${y_ball()} \n`
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

    fs.writeFileSync(
      `./close_region_logs/checkLog${close_region_count}.csv`, 
      "t, y_fer, y_ball, \n" + log
    )
  }
}

max_h = 0;
for(var h of heights){
  max_h = Math.max(h, max_h);
}

output_data = "Max Height Percentage, Count, Total Collision Count, Time increment tau[s], MaxH, StartH, Count of y_0' < y_max \n";
output_data += `,,${collision_count}, ${τ}, ${max_h}, ${h_0}, ${close_region_count} \n` 

// CREATE HISTOGRAM
for (var i = 0; i < height_categories; i++) {
  cnt = heights.filter(
    (x) =>
      x > (max_h * i) / height_categories &&
      x <= (max_h * (i + 1)) / height_categories
  ).length;

  output_data += `${(100 * i) / height_categories}%, ${cnt}\n`;
}

fs.writeFileSync(`output.csv`, output_data);
