const { run_sims } = require("../sim_RK.js");

const {
    Worker,
    isMainThread,
    parentPort,
    workerData
} = require("worker_threads");

const worker_count = 6;
if (isMainThread) {
    // // iter 1 - zoom on 1:2 mode
    // ds = []
    // for (var d = 8.4; d <= 9.3; d += 0.0025) {
    //     ds.push(d)
    // }
    // ks = []
    // for (var k = 0.5; k <= 0.78; k += 0.01) {
    //     ks.push(k)
    // }

    // // iter 2 - initial velocity change
    // o1s = []
    // for (var o = 0.25; o <= 100; o += 0.01) {
    //     o1s.push(o)
    // }
    // ks = []
    // for (var k = 0.95; k <= 1.6; k += 0.001) {
    //     ks.push(k)
    // }
    // ds = [8]

    // // iter 3 - angle change
    // ks = []
    // for (var k = 0.2; k <= 2.5; k += 0.02) {
    //     ks.push(k)
    // }
    // ds = [7.2, 8.7]
    // angs = []
    // for (var ang = 0; ang <= 2*Math.PI/3; ang += 2*Math.PI/3 * 1/120) { // increment by 1 degree
    //     angs.push(ang)
    // }
    // console.log(angs)

    o1s = []
    for (var o = 44; o <= 52; o += 0.02) {
        o1s.push(o)
    }
    ks = []
    for (var k = 1.09; k <= 1.13; k += 0.001) {
        ks.push(k)
    }
    ds = [8]

    for(var i = 0; i< worker_count; i++){
        console.log(ks.filter((k,id) => id%worker_count == i))
        let worker = new Worker(__filename, { workerData: {
            ks: ks.filter((k,id) => id%worker_count == i),
            ds: ds,
            o1s: o1s
        }});

        worker.on("message", msg => console.log(`Worker message received: ${msg}`));
        worker.on("error", err => console.error(error));
        worker.on("exit", code => console.log(`Worker exited with code ${code}.`));
    }
}
else {
    const data = workerData;
    run_sims(
        data.ds,
        data.o1s,
        data.ks,
        data.angs,
        data.ts
    )
}


// console.log(ds.length, ks.length)