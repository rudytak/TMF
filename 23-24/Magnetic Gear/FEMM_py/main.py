from contextlib import nullcontext
from webbrowser import get
import femm
import os

from types import SimpleNamespace

class FEMMProblemMI:
    def __init__(self,
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
            hide=False):

        self.problem_type = 0 
        self.freq = freq
        self.units = units
        self.field_type = field_type
        self.precision = precision
        self.depth = depth
        self.minangle = minangle
        self.acsolver = (0 if acsolver=="successive_approximation" else 1)
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
            self.acsolver
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

    def create_simulation_domain(self, padding = 1):
        min_x = 1e10
        min_y = 1e10

        max_x = -1e10
        max_y = -1e10

        for o in self.objects:
            _aabb = o.get_AABB()

            min_x = min(min_x, _aabb[0][0])
            min_y = min(min_y, _aabb[0][1])

            max_x = max(max_x, _aabb[1][0])
            max_y = max(max_y, _aabb[1][1])
        
        if(len(self.objects) < 1):
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

        femm.mi_addboundprop("A1",0,0,0,0,0,0,0,0,0)
        femm.mi_selectsegment(min_x, min_y)
        femm.mi_selectsegment(max_x, min_y)
        femm.mi_selectsegment(max_x, max_y)
        femm.mi_selectsegment(min_x, max_y)
        femm.mi_setsegmentprop("A1", 0,1,0,0)

        femm.mi_clearselected()
        femm.mi_addblocklabel(
            min_x + padding/10,
            min_y + padding/10
        )
        femm.mi_selectlabel(
            min_x + padding/10,
            min_y + padding/10
        )
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
        femm.mo_showdensityplot(1,0,_max,_min,prop)

    def show_vector_plot(self, typ, scale = 1):
        # 0 for no vector plot
        # 1 for the real part of flux density B
        # 2 for the real part of field intensity H
        # 3 for the imaginary part of B
        # 4 for the imaginary part of H
        # 5 for both the real and imaginary parts of B
        # 6 for both the real and imaginary parts of H
        femm.mo_showvectorplot(typ, scale)

    def rect(self,x,y,w,h):
        o = RectMI(x,y,w,h)
        self.objects.append(o)
        return o

class RectMI:
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h

        self.drawn = False

    def get_AABB(self):
        return [
            [
                self.x-self.w/2,
                self.y-self.h/2
            ],[ # bottom left point
                self.x+self.w/2,
                self.y+self.h/2
            ]  # top right point
        ]

    def draw(self):
        x1=self.x-self.w/2
        x2=self.x+self.w/2
        y1=self.y-self.h/2
        y2=self.y+self.h/2

        self.drawn = True

        femm.mi_drawrectangle(x1,y1,x2,y2)
    
    def set_material(self, material, magnetization_ang = 0):
        femm.mi_clearselected()
        femm.mi_addblocklabel(
            self.x,
            self.y
        )
        femm.mi_selectlabel(
            self.x,
            self.y
        )
        femm.mi_setblockprop(material, 1, 1, 0, magnetization_ang, 0, 0)
        femm.mi_clearselected()

if(__name__=="__main__"):
    P = FEMMProblemMI(0, field_type="planar")
    P.get_materials([
        "Air",
        "N42",
        "M-36 Steel"
    ])

    r1 = P.rect(0,0,30,15)
    r1.draw()
    r1.set_material("N42", 0)

    r2 = P.rect(22.5,7.5,15,30)
    r2.draw()
    r2.set_material("N42", -90)

    r3 = P.rect(45,0,30,15)
    r3.draw()
    r3.set_material("N42", -180)

    r4 = P.rect(67.5,7.5,15,30)
    r4.draw()
    r4.set_material("N42", -270)

    r5 = P.rect(90,0,30,15)
    r5.draw()
    r5.set_material("N42", -360)

    P.create_simulation_domain(30)
    P.save("./output", "test")
    P.calculate_solution()

    P.show_density_plot("bmag", 1, 0)
    # P.show_vector_plot(5, 1)
    input()