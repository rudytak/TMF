import femm
import os

import math, numpy


class v2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def toTuple(self):
        return (self.x, self.y)

    def __add__(self, o):
        return v2(self.x + o.x, self.y + o.y)

    def __mult__(self, k):
        return v2(self.x * k, self.y * k)

    def rotate(self, origin, angle):
        rot = v2.rotate(origin, self, angle)
        self.x = rot.x
        self.y = rot.y

    @staticmethod
    def rotate(point, origin, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin.toTuple()
        px, py = point.toTuple()

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return v2(qx, qy)


class FEMMProblemMI:
    def __init__(
        self,
        problem_type,
        # 0 for a magnetics problem
        # 1 for an electrostatics problem
        # 2 for a heat flow problem
        # 3 for a current flow problem
        freq=0,
        units="millimeters",
        # "inches"|"millimeters"|"centimeters"|"mils"|"meters"|"micrometers",
        field_type="planar",
        # "planar"|"axi",
        precision=1e-8,
        depth=0,
        minangle=30,
        acsolver="successive_approximation",
        # "successive_approximation"|"Newton"
        hide=False,
    ):
        self.problem_type = 0
        self.freq = freq
        self.units = units
        self.field_type = field_type
        self.precision = precision
        self.depth = depth
        self.minangle = minangle
        self.acsolver = 0 if acsolver == "successive_approximation" else 1
        self.hide = hide

        femm.openfemm(self.hide)

        femm.newdocument(self.problem_type)

        femm.mi_probdef(
            self.freq,
            self.units,
            self.field_type,
            self.precision,
            self.depth,
            self.minangle,
            self.acsolver,
        )

        self.materials = []
        self.objects = []

    def get_materials(self, materials):
        for m in materials:
            femm.mi_getmaterial(m)
            self.materials.append(m)

    def save(self, path, name):
        os.makedirs(path, exist_ok=True)
        femm.mi_saveas(path + "/" + name + ".fem")

    def create_simulation_domain(self, padding=1):
        min_x = 1e10
        min_y = 1e10

        max_x = -1e10
        max_y = -1e10

        for o in self.objects:
            _aabb = o.AABB

            min_x = min(min_x, _aabb[0].x)
            min_y = min(min_y, _aabb[0].y)

            max_x = max(max_x, _aabb[1].x)
            max_y = max(max_y, _aabb[1].y)

        if len(self.objects) < 1:
            min_x = min_y = max_x = max_y = 0

        min_x -= padding
        min_y -= padding

        max_x += padding
        max_y += padding

        femm.mi_clearselected()

        femm.mi_addnode(min_x, min_y)
        femm.mi_addnode(max_x, min_y)
        femm.mi_addnode(max_x, max_y)
        femm.mi_addnode(min_x, max_y)
        femm.mi_addsegment(min_x, min_y, min_x, max_y)
        femm.mi_addsegment(max_x, min_y, min_x, min_y)
        femm.mi_addsegment(max_x, max_y, max_x, min_y)
        femm.mi_addsegment(min_x, max_y, max_x, max_y)

        femm.mi_addboundprop("A1", 0, 0, 0, 0, 0, 0, 0, 0, 0)
        femm.mi_selectsegment(min_x, min_y)
        femm.mi_selectsegment(max_x, min_y)
        femm.mi_selectsegment(max_x, max_y)
        femm.mi_selectsegment(min_x, max_y)
        femm.mi_setsegmentprop("A1", 0, 1, 0, 0)

        femm.mi_clearselected()
        femm.mi_addblocklabel(min_x + padding / 10, min_y + padding / 10)
        femm.mi_selectlabel(min_x + padding / 10, min_y + padding / 10)
        femm.mi_setblockprop("Air", 1, 1, 0, 0, 0, 0)
        femm.mi_clearselected()

        femm.mi_zoomnatural()

    def calculate_solution(self):
        femm.mi_createmesh()
        femm.mi_analyze(0)
        femm.mi_loadsolution()

    def show_density_plot(self, prop, _max, _min):
        # bmag / breal / bimag / logb
        # hmag / hreal / himag / logh
        # jmag / jreal / jimag / logj
        femm.mo_showdensityplot(1, 0, _max, _min, prop)

    def show_vector_plot(self, typ, scale=1):
        # 0 for no vector plot
        # 1 for the real part of flux density B
        # 2 for the real part of field intensity H
        # 3 for the imaginary part of B
        # 4 for the imaginary part of H
        # 5 for both the real and imaginary parts of B
        # 6 for both the real and imaginary parts of H
        femm.mo_showvectorplot(typ, scale)

    def rect(self, x, y, w, h, ang):
        o = RectMI(x, y, w, h, ang)
        self.objects.append(o)
        return o


class RectMI:
    def __init__(self, x, y, w, h, ang):
        # pos
        self.x = x
        self.y = y
        self.c = v2(self.x, self.y)

        # size
        self.w = w
        self.h = h
        self.s = v2(self.w, self.h)

        # angle
        self.ang_deg = ang
        self.ang = ang * math.pi / 180

        self.rt = v2.rotate(
            v2(self.x + self.w / 2, self.y - self.h / 2), self.c, self.ang
        )
        self.lt = v2.rotate(
            v2(self.x - self.w / 2, self.y - self.h / 2), self.c, self.ang
        )
        self.lb = v2.rotate(
            v2(self.x - self.w / 2, self.y + self.h / 2), self.c, self.ang
        )
        self.rb = v2.rotate(
            v2(self.x + self.w / 2, self.y + self.h / 2), self.c, self.ang
        )

        # AABB
        self.AABB = [
            v2(
                min([self.rt.x, self.lt.x, self.lb.x, self.rb.x]),
                min([self.rt.y, self.lt.y, self.lb.y, self.rb.y]),
            ),
            v2(
                max([self.rt.x, self.lt.x, self.lb.x, self.rb.x]),
                max([self.rt.y, self.lt.y, self.lb.y, self.rb.y]),
            ),
        ]

        self.drawn = False

    def draw(self):
        femm.mi_drawline(self.lt.x, self.lt.y, self.rt.x, self.rt.y)
        femm.mi_drawline(self.rt.x, self.rt.y, self.rb.x, self.rb.y)
        femm.mi_drawline(self.rb.x, self.rb.y, self.lb.x, self.lb.y)
        femm.mi_drawline(self.lb.x, self.lb.y, self.lt.x, self.lt.y)
        self.drawn = True

    def set_material(self, material, rel_magnetization_ang=0):
        femm.mi_clearselected()
        femm.mi_addblocklabel(self.x, self.y)
        femm.mi_selectlabel(self.x, self.y)
        femm.mi_setblockprop(
            material, 1, 1, 0, self.ang_deg + rel_magnetization_ang, 0, 0
        )
        femm.mi_clearselected()


s = 1
if __name__ == "__main__":
    P = FEMMProblemMI(0, field_type="planar")
    P.get_materials(["Air", "N42", "M-36 Steel"])

    # outer ring

    # inner ring

    # modulator

    a_inc = 15
    for a in numpy.arange(0, 360, 2 * a_inc):
        x_1 = math.cos(a * math.pi / 180) * 25 * s
        y_1 = math.sin(a * math.pi / 180) * 25 * s

        r_1 = P.rect(x_1, y_1, 3 * s, 4 * s, a)
        r_1.draw()
        r_1.set_material("N42")

        y_2 = math.sin((a + a_inc) * math.pi / 180) * 25 * s
        x_2 = math.cos((a + a_inc) * math.pi / 180) * 25 * s

        r_2 = P.rect(x_2, y_2, 3 * s, 4 * s, a + a_inc + 180)
        r_2.draw()
        r_2.set_material("N42")

    a_inc = 22.5
    for a in numpy.arange(0, 360, 2 * a_inc):
        x_1 = math.cos(a * math.pi / 180) * 20 * s
        y_1 = math.sin(a * math.pi / 180) * 20 * s

        r_1 = P.rect(x_1, y_1, 3 * s, 4 * s, a)
        r_1.draw()
        r_1.set_material("M-36 Steel")

        y_2 = math.sin((a + a_inc) * math.pi / 180) * 20 * s
        x_2 = math.cos((a + a_inc) * math.pi / 180) * 20 * s

        r_2 = P.rect(x_2, y_2, 3 * s, 4 * s, a + a_inc + 180)
        r_2.draw()
        r_2.set_material("M-36 Steel")

    a_inc = 45
    for a in numpy.arange(0, 360, 2 * a_inc):
        x_1 = math.cos(a * math.pi / 180) * 15 * s
        y_1 = math.sin(a * math.pi / 180) * 15 * s

        r_1 = P.rect(x_1, y_1, 3 * s, 4 * s, a)
        r_1.draw()
        r_1.set_material("N42")

        x_2 = math.cos((a + a_inc) * math.pi / 180) * 15 * s
        y_2 = math.sin((a + a_inc) * math.pi / 180) * 15 * s

        r_2 = P.rect(x_2, y_2, 3 * s, 4 * s, a + a_inc + 180)
        r_2.draw()
        r_2.set_material("N42")

    P.create_simulation_domain(5)
    P.save("./output", "test")
    P.calculate_solution()

    P.show_density_plot("bimag", 0.4, 0.2)
    # P.show_vector_plot(5, 1)
    input()
