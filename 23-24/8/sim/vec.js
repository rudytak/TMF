// vectors
class v3 {
  constructor(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }

  mult(k) {
    return v(this.x * k, this.y * k, this.z * k);
  }
  unit() {
    return this.mult(1 / this.mag());
  }
  mag() {
    return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
  }

  add(v2) {
    return v3.add(this, v2);
  }

  sub(v2) {
    return v3.sub(this, v2);
  }

  static add(v1, v2) {
    return v(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z);
  }

  static add_many(v_arr) {
    return v(
      v_arr.reduce((c, v) => c + v.x, 0),
      v_arr.reduce((c, v) => c + v.y, 0),
      v_arr.reduce((c, v) => c + v.z, 0)
    );
  }

  static sub(v1, v2) {
    return v(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);
  }

  static dot(v1, v2) {
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
  }

  static cross(v1, v2) {
    return new v(
      v1.y * v2.z - v1.z * v2.y,
      v1.x * v2.z - v1.z * v2.x,
      v1.x * v2.y - v1.y * v2.x
    );
  }
}
v3.prototype.toString = function () {
  return { x: this.x, y: this.y, z: this.z }.toString();
};
function v(x, y, z = 0) {
  return new v3(x, y, z);
}

module.exports = {
    v3: v3,
    v: v
}
