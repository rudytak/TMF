const { v3, v } = require("../vec.js");
const {
    sim_instance,
    RK_matrix
} = require("./sim_RK_old.js");

// spinner creation
let si = new sim_instance({ dt: 1e-2, run_time: 30, out_path: "out_old.csv" }, RK_matrix.RK4);
si.add_spinner(v(0, 0, 0), 0, 7.5);
si.add_spinner(v(0.08, 0, 0), 0, -10, true);

// large permanent magnet
// si.add_spinner(v(0, 0.08, 0), 0, 0, true, 0, 0, "vertical", 1, 0, 1, (1 / sim_instance.constants.μ_0) * 1.4 * 0.047 * 0.022 * 0.0095);

si.run();