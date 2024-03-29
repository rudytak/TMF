const { v3, v } = require("../vec.js");
const { sim_instance, RK_matrix } = require("../sim_RK.js");
const fs = require("fs");

for (var d = 7; d < 20; d += 0.0) {
  for (var o1 = 10; o1 <= 10; o1 += 0.1) {
    for (var k = 0; k <= 7; k += 0.00) {
      if (
        !fs.existsSync(
          `./runs/d=${d.toFixed(2)}_o=${o1.toFixed(2)}_k=${k.toFixed(3)}.csv`
        )
      ) {
        console.log("Start:", d.toFixed(2), o1.toFixed(2), k.toFixed(3));

        // spinner creation
        let si = new sim_instance(
          {
            dt: 1e-4,
            save_freq: 1e2,
            end_time: 25,
            out_path: `./runs/d=${d.toFixed(2)}_o=${o1.toFixed(
              2
            )}_k=${k.toFixed(3)}.csv`,
            exports: ["s[1].omega / s[0].omega"],
          },
          RK_matrix.RK4,
          {
            α: 0.218,
            γ: 0.000259,
          }
        );
        si.add_spinner(v(0, 0, 0), 0, o1, true);
        si.add_spinner(v(d / 100, 0, 0), 0, -k * o1);

        // large permanent magnet
        // si.add_spinner(v(0, 0.08, 0), 0, 0, true, 0, 0, "vertical", 1, 0, 1, (1 / sim_instance.constants.μ_0) * 1.4 * 0.047 * 0.022 * 0.0095);

        si.run();
      }else{
        console.log("Already done:", d.toFixed(2), o1.toFixed(2), k.toFixed(3));
      }

      if(k < 2){
        k += 0.01
      }else if(k < 4){
        k += 0.025
      }else{
        k += 0.1
      }

      k = Math.round(k * 1000) / 1000;
    }
    o1 = Math.round(o1 * 100) / 100;
  }

  if(d < 10){
    d += 0.1
  }else if(d < 14){
    d += 0.25
  }else{
    d += 0.5
  }

  d = Math.round(d * 100) / 100;
}
