var engine, render, runner;

var W = 1; // m
var H = 1; // m

const FRICTION = 0;
const DENSITY = 7500; // 7300 - 7700 kg/m^3
const REMENANCE = 1.1; // 1 - 1.5 T
var scaling = 200; // = m/px

// create dipoles
var d1 = new DipoleSphere(.1, .3, 0.0125)
var d2 = new DipoleSphere(.3, .3, 0.0125)
console.log(d1, d2)

console.log()

function resize(w,h,n_s){
    oldx1 = d1.x;
    oldy1 = d1.y;

    oldx2 = d2.x;
    oldy2 = d2.y;

    scaling = n_s
    W = w;
    H = h

    d1.x = oldx1;
    d1.y = oldy1;

    d2.x = oldx2;
    d2.y = oldy2;

    delete engine, render, runner;

    var c = document.querySelector("canvas");
    c.parentElement.removeChild(c);

    init();
    run();
}

const gui = new dat.GUI();

gui.add({
    get W() {
        return W
    },
    set W(n_W) {
        resize(n_W,H,scaling);
    }
}, "W", 0.01, 10);
gui.add({
    get H() {
        return H
    },
    set H(n_H) {
        resize(W,n_H,scaling);
    }
}, "H", 0.01, 10);
gui.add({
    get s() {
        return scaling
    },
    set s(n_s) {
        resize(W,H,n_s);
    }
}, "s", 10, 1000);

var df1 = gui.addFolder("Dipole 1")
df1.add(d1, 'x', 0, W, 0.001)
df1.add(d1, 'y', 0, H, 0.001)
df1.add(d1, 'r', 0.0001, 2 * W, 0.0001)//.listen()
df1.add(d1, 'm', 0.0001, 4 / 3 * Math.PI * (2 * W) * 10000, 0.001)//.listen()
df1.add(d1, 'B_r', 0, 3, 0.001)
df1.add(d1, 'ρ', 0, 10000, 1)
df1.open()
// df1.add(cube.rotation, 'z', 0, Math.PI * 2)

var df2 = gui.addFolder("Dipole 2")
df2.add(d2, 'x', 0, W, 0.001)
df2.add(d2, 'y', 0, H, 0.001)
df2.add(d2, 'r', 0.0001, 2 * W, 0.0001)//.listen()
df2.add(d2, 'm', 0.0001, 4 / 3 * Math.PI * (2 * W) * 10000, 0.001)//.listen()
df2.add(d2, 'B_r', 0, 3, 0.001)
df2.add(d2, 'ρ', 0, 10000, 1)
df2.open()
// df2.add(cube.rotation, 'z', 0, Math.PI * 2)

gui.width = 600;


function init() {
    {
        // create an engine
        engine = Engine.create();
        // turn off gravity
        engine.world.gravity.y = 0;

        // create a renderer
        render = Render.create({
            element: document.body,
            engine: engine,
            options: {
                height: H * scaling,
                width: W * scaling
            }
        });

        drawScale(engine.world)
    }

    // ADD dipoles to the scene
    d1.add(engine.world);
    d2.add(engine.world);
}

function run() {
    // run the renderer
    Render.run(render);
    // create runner
    runner = Runner.create();
    // run the engine
    Runner.run(runner, engine);
}

function runSim() {
    console.log("running sim")
}

init();
run();