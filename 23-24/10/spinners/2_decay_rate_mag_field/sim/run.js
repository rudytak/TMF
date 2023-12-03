const { v3, v } = require("../../sim/vec.js");
const {
    sim_instance,
    RK_matrix
} = require("../../sim/sim_RK.js");

//simulation for spinner 1
let si = new sim_instance(
    { dt: 2.5e-5, run_time: 35, out_path: "sim_spinner_magnetic1.csv" },
    RK_matrix.RK4,
    {
        α: 0.868,
        γ: 0.000655
    }
);
si.add_spinner(v(0, 0, 0), 0, 42.79037740851004);
si.add_spinner(
    v(0, 0.085 + 0.011, 0), 
    0,
    0,
    true,
    0,
    0,
    "vertical",
    1,
    0,
    1,
    (1 / sim_instance.constants.μ_0) * 0.8701359766320094 * 0.047 * 0.022 * 0.0095);

si.run();