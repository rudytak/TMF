const {
    sim_instance,
    RK_matrix
} = require("../../sim_RK.js");
const { v3, v } = require("../../vec.js");

// spinner creation
let si = new sim_instance({ dt: 1e-4, run_time: 30, out_path: "out_eu_new.csv" }, RK_matrix.Euler);
si.add_spinner(v(0, 0, 0), 0, 7.5);
si.add_spinner(v(0.08, 0, 0), 0, -10, true);
si.run();

let si2 = new sim_instance({ dt: 1e-4, run_time: 30, out_path: "out_mid.csv" }, RK_matrix.Midpoint);
si2.add_spinner(v(0, 0, 0), 0, 7.5);
si2.add_spinner(v(0.08, 0, 0), 0, -10, true);
si2.run();

let si3 = new sim_instance({ dt: 1e-4, run_time: 30, out_path: "out_heun.csv" }, RK_matrix.Heun2);
si3.add_spinner(v(0, 0, 0), 0, 7.5);
si3.add_spinner(v(0.08, 0, 0), 0, -10, true);
si3.run();

let si4 = new sim_instance({ dt: 1e-4, run_time: 30, out_path: "out_ral2.csv" }, RK_matrix.Ralston2);
si4.add_spinner(v(0, 0, 0), 0, 7.5);
si4.add_spinner(v(0.08, 0, 0), 0, -10, true);
si4.run();

let si5 = new sim_instance({ dt: 1e-4, run_time: 30, out_path: "out_rk3-8.csv" }, RK_matrix.RK_3_8);
si5.add_spinner(v(0, 0, 0), 0, 7.5);
si5.add_spinner(v(0.08, 0, 0), 0, -10, true);
si5.run();

let si6 = new sim_instance({ dt: 1e-4, run_time: 30, out_path: "out_rk4.csv" }, RK_matrix.RK4);
si6.add_spinner(v(0, 0, 0), 0, 7.5);
si6.add_spinner(v(0.08, 0, 0), 0, -10, true);
si6.run();

let si7 = new sim_instance({ dt: 1e-4, run_time: 30, out_path: "out_ral4.csv" }, RK_matrix.Ralston4);
si7.add_spinner(v(0, 0, 0), 0, 7.5);
si7.add_spinner(v(0.08, 0, 0), 0, -10, true);
si7.run();