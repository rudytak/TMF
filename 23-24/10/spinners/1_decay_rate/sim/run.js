const { v3, v } = require("../../sim/vec.js");
const {
    sim_instance,
    RK_matrix
} = require("../../sim/sim_RK.js");

//simulation for spinner 1
let si = new sim_instance(
    { dt: 1e-4, run_time: 30, out_path: "sim_spinner1.csv" },
    RK_matrix.RK4,
    {
        α: 0.218,
        γ: 0.000259
    }
);
si.add_spinner(v(0, 0, 0), 0, 115.41914281371224);
si.run();