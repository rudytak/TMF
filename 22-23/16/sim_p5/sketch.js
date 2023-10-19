let H = 100;
let W = (l / (2 * r)) * H;
let PAD = 65;

let plt = {
  x: {
    _min: 0,
    _max: 1e-2,
    _inc: 1e-3,
    name: "time/s",
    w: 600,
  },
  y: {
    h: 400,
    measurements: [
      //{
      //  _min: -25e4,
      //  _max: 25e4,
      //  _inc: 1e5,
      //  col: "green",
      //  name: "P/W",
      //  points: []
      //},
      //{
      //  _min: -1e4,
      //  _max: 1e4,
      //  _inc: 1e5,
      //  col: "blue",
      //  name: "p/Pa",
      //  points: []
      //},
      {
        _min: 0,
        _max: .03,
        _inc: 1e-2,
        col: "red",
        name: "Qh/J",
        points: []
      },
      {
        _min: 0,
        _max: .001,
        _inc: 1e-4,
        col: "blue",
        name: "Qc/J",
        points: []
      },
    ],
  },
};
function addDataVal(name, x, y){
  plt.y.measurements.find(m => m.name == name)?.points.push([x,y]);
}

function drawPlt() {
  push();
  translate(PAD, 2 * PAD + H);

  // BG
  fill("white");
  rect(0, 0, plt.x.w, plt.y.h);

  // TEXT AND LINES X
  textAlign(LEFT, TOP);
  for (let i = plt.x._min; i < plt.x._max + plt.x._inc/2; i += plt.x._inc) {
    let x_pos = (plt.x.w * (i - plt.x._min)) / (plt.x._max - plt.x._min);

    fill("black");
    noStroke();
    text(round(i, 9), x_pos, plt.y.h);

    noFill();
    stroke("lightgray");
    line(x_pos, 0, x_pos, plt.y.h);
  }
  fill("black");
  noStroke();
  text(plt.x.name, plt.x.w, plt.y.h + PAD / 2);

  // TEXT AND LINES Y
  for (let m = 0; m < plt.y.measurements.length; m++) {
    measurement = plt.y.measurements[m]
    textAlign(RIGHT, TOP);
    for (let i = measurement._min; i < measurement._max + measurement._inc / 2; i += measurement._inc) {
      let y_pos = plt.y.h * (1 - (i - measurement._min) / (measurement._max - measurement._min));

      fill(measurement.col);
      noStroke();
      text(round(i, 9), 0, y_pos);

      noFill();
      let trans_c = color(measurement.col)
      trans_c.setAlpha(100)
      stroke(trans_c);
      line(0, y_pos, plt.x.w, y_pos);
    }
    textAlign(LEFT, TOP);
    fill(measurement.col);
    noStroke();
    text(measurement.name, -PAD, m * 15);
    
    // DATA POINTS
    stroke(measurement.col);
    strokeWeight(2);
    noFill();
    for(let p of measurement.points){
      let x = (plt.x.w * (p[0] - plt.x._min)) / (plt.x._max - plt.x._min)
      let y = plt.y.h * (1 - (p[1] - measurement._min) / (measurement._max - measurement._min))
      
      point(x,y)
    }
  }

  pop();
}

function setup() {
  let c = createCanvas(1.5 * W + 2 * PAD, H + 2 * PAD + plt.y.h + PAD);
}

function draw() {
  background(220);

  push();
  translate(PAD, PAD);

  // TEST TUBE
  noFill();
  stroke("black");
  strokeWeight(3);

  line(0, 0, 0, H);
  line(0, 0, W, 0);
  line(0, H, W, H);

  // HEATERS
  for (let i = 0; i < heaters.length; i++) {
    h = heaters[i];
    stroke(col_fromT(h.temp));
    line(
      (h.start / l) * W,
      -PAD / 3 - i * 4,
      (h.end / l) * W,
      -PAD / 3 - i * 4
    );
  }

  // FRAME TEXT
  noStroke();
  fill("black");
  textAlign(LEFT, TOP);
  text(round(sim_t, 9) + "s \n frame: " + frameCount, -PAD, H + 3);

  // LAYERS
  noFill();
  stroke("black");
  strokeWeight(1);
  let totD = 0;
  for (let lay of layers) {
    fill(col_fromT(lay.T));
    rect((W * totD) / l, 0, (W * lay.d) / l, H);

    //push();
    //stroke("white")
    //fill("white")
    //rotate(Math.PI/2)
    //text(lay.T + "\n" + lay.p, 0, -W * totD / l)
    //pop();

    totD += lay.d;
  }
  pop();

  drawPlt();

  // SIMULATION
  sim_t = tau * frameCount;
  iter().forEach(
    to_plot => addDataVal(...to_plot)
  );
}

function col_fromT(T) {
  const T_blue = absZ;
  const T_red = 1100 + absZ;
  return lerpColor(
    color("blue"),
    color("red"),
    (T - T_blue) / (T_red - T_blue)
  );
}