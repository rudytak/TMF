const { run_sims } = require("../sim_RK.js");

const {
    Worker,
    isMainThread,
    parentPort,
    workerData
} = require("worker_threads");

const worker_count = 8;
if (isMainThread) {
    ds = []
    for (var d = 8.4; d <= 9.3; d += 0.0025) {
        ds.push(d)
    }
    ks = []
    for (var k = 0.5; k <= 0.78; k += 0.01) {
        ks.push(k)
    }

    for(var i = 0; i< worker_count; i++){
        console.log(ks.filter((k,id) => id%worker_count == i))
        let worker = new Worker(__filename, { workerData: {
            ks: ks.filter((k,id) => id%worker_count == i),
            ds: ds
        } });

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
