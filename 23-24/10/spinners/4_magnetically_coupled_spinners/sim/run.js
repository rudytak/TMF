const { v3, v } = require("../../sim/vec.js");
const {
    sim_instance,
    RK_matrix
} = require("../../sim/sim_RK.js");

// //simulation for spinner 1:1
let si = new sim_instance(
    { dt: 1e-4, end_time: 20, out_path: "1_to_1_3.1V.csv", start_time: 2.74, exports: ["-s[0].ω", "-s[0].φ"] },
    RK_matrix.RK4,
    {
        α: 0.218,
        // β: 0.000188,
        γ: 0.000268
    }
);
si.add_spinner(v(0, 0, 0), Math.PI/6, -9.86);
si.add_spinner(v(0, 0.08, 0), 0, 9.86, true);
si.run();

// //simulation for spinner 1:2
let si2 = new sim_instance(
    { dt: 1e-4, end_time: 26, out_path: "1_to_2_3.1V.csv", start_time: 15.59, exports: ["-s[0].ω", "-s[0].φ"] },
    RK_matrix.RK4,
    {
        α: 0.686,
        // β: 0.000188,
        γ: 0.000655
    }
);
si2.add_spinner(v(0, 0, 0), 0, -4.8);
si2.add_spinner(v(0.08, 0, 0), 0, 9.86, true);
si2.run();

// //simulation for spinner 2:1
let si3 = new sim_instance(
    { dt: 1e-4, end_time: 20, out_path: "2_to_1_2.6V.csv", start_time: 0.78, exports: ["-s[0].ω", "-s[0].φ"] },
    RK_matrix.RK4,
    {
        α: 0.686,
        //β: 0.000188,
        γ: 0.000655
    }
);
si3.add_spinner(v(0, 0, 0), 0, -15.26, false);
si3.add_spinner(v(0, 0.08, 0), 0, 7.85, true);
si3.run();