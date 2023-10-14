//HELPER FUNCTIONS
function v(x, y, z = 0) {
    return {
        x: x,
        y: y,
        z: z
    }
}

// CONVERSION
function CylinderVolume_to_SphereRadius(r, h) {
    var R = Math.pow(3 / 4 * r * r * h, 1 / 3)

    return R;
}

function drawScale(e) {
    var line = Bodies.rectangle(
        10 + scaling / 2,
        10,
        scaling, 3,
        {
            isStatic: true,
            isSensor: true
        }
    );

    Composite.add(e, line);
}

// module aliases
var Engine = Matter.Engine,
    Render = Matter.Render,
    Runner = Matter.Runner,
    Body = Matter.Body,
    Bodies = Matter.Bodies,
    Composite = Matter.Composite;

class DipoleSphere {
    constructor(x, y, r) {
        this._ρ = DENSITY;
        this.B_r = REMENANCE;

        this.instance = Bodies.circle(
            x * scaling,
            y * scaling,
            r * scaling,
            {
                friction: FRICTION,
                frictionAir: FRICTION,
                frictionStatic: FRICTION,
                mass: 4 / 3 * Math.PI * r * r * r * this.ρ,
                inverseMass: 1 / (4 / 3 * Math.PI * r * r * r * this.ρ),
                isSensor: true
            }
        );
    }

    get ρ() {
        return this._ρ;
    }

    set ρ(n_ρ) {
        this._ρ = n_ρ;

        this.m = 4 / 3 * Math.PI * this.r * this.r * this.r * n_ρ;
    }

    get r() {
        return this.instance.circleRadius / scaling
    }

    set r(n_r) {
        var old = this.instance;

        this.instance = Bodies.circle(
            old.position.x,
            old.position.y,
            n_r * scaling,
            {
                friction: FRICTION,
                frictionAir: FRICTION,
                frictionStatic: FRICTION,
                mass: 4 / 3 * Math.PI * n_r * n_r * n_r * this.ρ,
                inverseMass: 1 / (4 / 3 * Math.PI * n_r * n_r * n_r * this.ρ),
                isSensor: true
            }
        );

        Composite.remove(engine.world, old, true);
        this.add(engine.world)

        gui.updateDisplay();
    }

    get m() {
        return this.instance.mass
    }

    set m(n_m) {
        this.r = Math.pow(3 * n_m / (4 * Math.PI * this.ρ), 1 / 3)
    }

    get x() {
        return this.instance.position.x / scaling
    }

    set x(n_x) {
        var vb = this.instance.velocity;

        Body.setPosition(this.instance, {
            x: n_x * scaling,
            y: this.instance.position.y
        })

        Body.setVelocity(this.instance, vb);
    }

    get y() {
        return this.instance.position.y / scaling
    }

    set y(n_y) {
        var vb = this.instance.velocity;

        Body.setPosition(this.instance, {
            x: this.instance.position.x,
            y: n_y * scaling
        })

        Body.setVelocity(this.instance, vb);
    }

    add(e) {
        console.log("Added")
        Composite.add(e, this.instance);
    }

    remove(e) {
        console.log("removed")
        Composite.remove(e, this.instance, true);
    }

    applyForce(v) {
        Body.applyForce(this.instance, this.instance.position, { x: v.x, y: v.y })
    }
}