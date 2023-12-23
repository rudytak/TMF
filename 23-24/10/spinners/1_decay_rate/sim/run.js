const { v3, v } = require("../../sim/vec.js");
const {
    sim_instance,
    RK_matrix
} = require("../../sim/sim_RK.js");

//simulation for spinner 1
let si = new sim_instance(
    { dt: 1e-3, end_time: 170, out_path: "sim_spinner1.csv" },
    RK_matrix.RK4,
    {
        α: 0.218,
        γ: 0.000259
    }
);
si.add_spinner(v(0, 0, 0), 0, 115.41914281371224);
si.run();

//simulation for spinner 1 with linear component
let si_lin = new sim_instance(
    { dt: 1e-3, end_time: 170, out_path: "sim_spinner1_with_beta.csv" },
    RK_matrix.RK4,
    {
        α: 0.22040868137353412,
        β: 0.00018882943185321167,
        γ: 0.00026124506671733165
    }
);
si_lin.add_spinner(v(0, 0, 0), 0, 115.41914281371224);
si_lin.run();