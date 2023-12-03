const { v3, v } = require("../../sim/vec.js");
const {
    sim_instance,
    RK_matrix
} = require("../../sim/sim_RK.js");

//simulation for spinner C0000
{
    let si = new sim_instance(
        { dt: 1e-3, run_time: 25, out_path: "C0000_SIM.csv", start_time: 1 },
        RK_matrix.RK4,
        {
            // α: 0.868,
            // γ: 0.000655
            α: 2.3448171228468498,
            β: 0.1,
            γ: 0.00038094028069841
        }
    );
    si.add_spinner(v(0, 0, 0), 2.10288682, 0);

    let big_rem = 0.8701359766320094
    // let big_rem = 0.923

    si.add_spinner(
        v(0.047 / 2, - 0.065 + 0.011, 0),
        0,
        0,
        true,
        0,
        0,
        0,
        "vertical",
        1,
        0,
        1,
        (0.2 / sim_instance.constants.μ_0) * big_rem * 0.047 * 0.022 * 0.0095);

    si.add_spinner(
        v(-0.047 / 2, - 0.065 + 0.011, 0),
        0,
        0,
        true,
        0,
        0,
        0,
        "vertical",
        1,
        0,
        1,
        (0.2 / sim_instance.constants.μ_0) * big_rem * 0.047 * 0.022 * 0.0095);

    si.add_spinner(
        v(0.047 / 2, - 0.065 - 0.011 / 2, 0),
        0,
        0,
        true,
        0,
        0,
        0,
        "vertical",
        1,
        0,
        1,
        (0.2 / sim_instance.constants.μ_0) * big_rem * 0.047 * 0.022 * 0.0095);

    si.add_spinner(
        v(-0.047 / 2, - 0.065 - 0.011 / 2, 0),
        0,
        0,
        true,
        0,
        0,
        0,
        "vertical",
        1,
        0,
        1,
        (0.2 / sim_instance.constants.μ_0) * big_rem * 0.047 * 0.022 * 0.0095);

    si.add_spinner(
        v(0, - 0.065 + 0.011 / 2, 0),
        0,
        0,
        true,
        0,
        0,
        0,
        "vertical",
        1,
        0,
        1,
        (0.2 / sim_instance.constants.μ_0) * big_rem * 0.047 * 0.022 * 0.0095);

    si.run();
}