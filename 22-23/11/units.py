import math;

# HELPER
def isNum(n):
    return type(n) == type(1) or type(n) == type(1.0)

def numPrec(n):
    return len(str(float(n)).split(".")[1])

def contains(a, b):
    # check if b is completely contained in a
    
    c = a.copy()
    d = b.copy()

    while len(d) != 0:
        el = d[0]
        if el in c:
            d.remove(el)
            c.remove(el)
        else: 
            return False

    return True

def nonzero_round(x,n):
    splt = f'{x:.16f}'.split(".")
    dec = f"{float('0.' + splt[1]):.{n}g}"

    return float(f'{int(x) + float(dec):.15f}')

class unit:
    def __init__(self, numerators, denominators, pre_simplify = False) -> None:
        if(numerators is None):
            self.numerators = []
        elif type(numerators) == type("str"):
            self.numerators = [numerators]
        else:
            self.numerators = numerators

        if(denominators is None):
            self.denominators = []
        elif type(denominators) == type("str"):
            self.denominators = [denominators]
        else:
            self.denominators = denominators

        self.pre_simplify = pre_simplify

        self.format()

    # UNIT SIMPLIFICATION    
    def copy(self):
        return unit(self.numerators, self.denominators, self.pre_simplify)

    def expand(self):
        # expand everything to SI units

        i = 0
        while i < self.numerators.__len__():
            n = self.numerators[i]

            if n in unit.equivalences.keys():
                self.numerators.remove(n)
                self.numerators += unit.equivalences[n][0]
                self.denominators += unit.equivalences[n][1]
                i-=1
            i+=1
        
        i = 0
        while i < self.denominators.__len__():
            d = self.denominators[i]
            
            if d in unit.equivalences.keys():
                self.denominators.remove(d)
                self.denominators += unit.equivalences[d][0]
                self.numerators += unit.equivalences[d][1]
                i-=1
            i+=1

        return self

    def shorten(self):
        # remove units that are in both denominator and numerator
        i=0
        while i < len(self.numerators):
            n = self.numerators[i]
            if n in self.denominators:
                self.numerators.remove(n)
                self.denominators.remove(n)
                i-=1
            i+=1
        
        return self
    
    def simplify(self):
        # create the shortest form from the expanded form

        for k in unit.equivalences.keys():
            nums_required = unit.equivalences[k][0]
            dens_required = unit.equivalences[k][1]

            retry = True
            while retry:
                retry = False

                if contains(self.numerators, nums_required) and contains(self.denominators, dens_required):
                    retry = True
                    
                    self.numerators.append(k)
                    
                    for n in nums_required:
                        self.numerators.remove(n)
                    for d in dens_required:
                        self.denominators.remove(d)
                
                if contains(self.numerators, dens_required) and contains(self.denominators, nums_required):
                    retry = True

                    self.denominators.append(k)
                    
                    for n in nums_required:
                        self.denominators.remove(n)
                    for d in dens_required:
                        self.numerators.remove(d)


        return self

    def format(self):
        self.expand()
        if self.pre_simplify:
            self.shorten()
        self.simplify()
        self.shorten()
    
    @property
    def f_nums(self):
        # unique unit
        unique_nums = list(set(self.numerators))
        return list(map(lambda u: f"{u}^{self.numerators.count(u)}" if self.numerators.count(u) > 1 else str(u), unique_nums))
        
    @property
    def f_dens(self):
        unique_dens = list(set(self.denominators))
        return list(map(lambda u: f"{u}^{self.denominators.count(u)}" if self.denominators.count(u) > 1 else str(u), unique_dens))

    # UNIT CONVERSION
    SI_units = [
        "kg",
        "s",
        "m",
        "A",
        "K",
        "mol",
        "cd"
    ]

    equivalences = {
    #   non-SI: numerators          denominators
        "V":    (["kg", "m", "m"],  ["A", "s", "s", "s"]),
        "J":    (["kg", "m", "m"],  ["s", "s"]),

        "W":    (["V", "A"],        []),
        "W":    (["J"],             ["s"]),
    }

    relations = {
    #   non-SI: factor  numerators         denominators
        "g":    (1e-3,  ["kg"],             []),
        "mm":   (1e-3,  ["m"],              []),
        "cm":   (1e-2,  ["m"],              []),
        "Hz":   (1,     [],                 ["s"]),
        "l":    (1e-3,  ["m", "m", "m"],    []),
        "ml":   (1e-6,  ["m", "m", "m"],    []),
        "pW":   (1e-12, ["W"],              []),
        "kJ":   (1e3,   ["J"],              [])
    }

    def gen_SI_selfconvert_factor(self):
        # generates a factor value, by which a var() instance can be converted into SI units

        # convert everything to SI units
        SI_f = var(1, 0, SI=False)

        for n in self.numerators:
            if n in unit.relations.keys():
                rel = unit.relations[n]
                SI_f = SI_f * var(rel[0], 0, rel[1], rel[2] + [n])
        
        for d in self.denominators:
            if d in unit.relations.keys():
                rel = unit.relations[d]
                SI_f = SI_f * var(1/rel[0], 0, rel[2] + [d], rel[1])

        return SI_f

    NONZERO_ROUNDING = 3

class var:
    # INIT
    def __init__(self, val:float, abs_dev:float = 0.0, unit_numerators:str|list = None, unit_denominators:str|list = None, SI = False, pre_simplify = True) -> None:
        self.val = val
        self.abs_dev = abs_dev

        self.unit = unit(unit_numerators, unit_denominators, pre_simplify)
        self.SI = SI
        self.pre_simplify = pre_simplify

        if self.SI:
            SI_f = self.unit.gen_SI_selfconvert_factor()
            self.unit = unit(self.unit.numerators + SI_f.unit.numerators, self.unit.denominators + SI_f.unit.denominators, self.pre_simplify)
            
            self.val *= SI_f.val
            self.abs_dev *= SI_f.val

    @property
    def rel_dev(self):
        return self.abs_dev / self.val

    @staticmethod
    def define_by_relative_deviation(val:float, rel_dev:float, unit:str|list = None, inv_unit:str|list = None, SI = False, simp = True):
        return var(val, val * rel_dev, unit, inv_unit, SI, simp)
    
    # FORMATTING
    # f = formatted
    # e = exact
    @property
    def f_numerators(self):
        return self.unit.f_nums
    
    @property
    def f_denominators(self):
        return self.unit.f_dens
    
    @property
    def e_numerators(self):
        return self.unit.copy().expand().f_nums
    
    @property
    def e_denominators(self):
        return self.unit.copy().expand().f_dens
    
    @property 
    def f_val(self):
        return nonzero_round(self.val, unit.NONZERO_ROUNDING)
    
    @property
    def ltx_val(self):
        spl = str(self.f_val).split("e")

        if(len(spl) == 1):
            return self.f_val
        else:
            return spl[0] + " \\cdot 10^{" + str(int(spl[1])) + "}"

    @property
    def f_abs_dev(self):
        return nonzero_round(self.abs_dev, unit.NONZERO_ROUNDING)
    
    @property
    def ltx_abs_dev(self):
        spl = str(self.f_abs_dev).split("e")

        if(len(spl) == 1):
            return self.f_abs_dev
        else:
            return spl[0] + " \\cdot 10^{" + str(int(spl[1])) + "}"

    @property
    def f_rel_dev(self):
        return nonzero_round(self.rel_dev * 100, unit.NONZERO_ROUNDING)

    @property
    def ltx_rel_dev(self):
        spl = str(self.f_rel_dev).split("e")

        if(len(spl) == 1):
            return self.f_rel_dev
        else:
            return spl[0] + " \\cdot 10^{" + str(int(spl[1])) + "}"

    # OPERATIONS
    def copy(self):
        return var(self.val, self.abs_dev, self.unit.numerators, self.unit_denominators)
    
    def __add__(self, u):
        if(isNum(u)):
            return self + var(u, 0)

        return var(
            self.val + u.val,
            self.abs_dev + u.abs_dev,
            self.unit.numerators,
            self.unit.denominators,
            self.SI, self.pre_simplify
        )
    
    def __sub__(self, u):
        if(isNum(u)):
            return self - var(u, 0)

        return var(
            self.val - u.val,
            self.abs_dev + u.abs_dev,
            self.unit.numerators,
            self.unit.denominators,
            self.SI, self.pre_simplify
        )

    def __mul__(self, u):
        if(isNum(u)):
            return self * var(u, 0)
        
        return var.define_by_relative_deviation(
            self.val * u.val,
            (self.rel_dev + u.rel_dev),
            self.unit.numerators + u.unit.numerators,
            self.unit.denominators + u.unit.denominators,
            self.SI, self.pre_simplify
        )

    def __truediv__(self, u):
        if(isNum(u)):
            return self / var(u, 0)
        
        return var.define_by_relative_deviation(
            self.val / u.val,
            (self.rel_dev + u.rel_dev),
            self.unit.numerators + u.unit.denominators,
            self.unit.denominators + u.unit.numerators,
            self.SI, self.pre_simplify
        )
    
    def __pow__(self, n):
        if(isNum(n)):
            return var.define_by_relative_deviation(
                pow(self.val, n),
                n * self.rel_dev,
                n * self.unit.numerators,
                n * self.unit.denominators,
            )
        else:
            return var.define_by_relative_deviation(
                pow(self.val, n.val),
                n.val * self.rel_dev,
                int(n.val) * self.unit.numerators,
                int(n.val) * self.unit.denominators
            )
    
    # STRINGIFICATIONS
    def __str__(self) -> str:
        out = f"{self.f_val}" + ("" if self.abs_dev == 0 else f" ± {self.f_abs_dev}")
        if len(self.f_denominators) == 0 and len(self.f_numerators) == 0:
            return out

        out += "1" if len(self.f_numerators) == 0 else f"{'*'.join([str(i) for i in self.f_numerators])}"
        out += f"/({'*'.join([str(i) for i in self.f_denominators])})" if len(self.f_denominators) > 0 else ""
        return out
    
    @property
    def ex(self) -> str:
        out = f"{self.val}" + ("" if self.abs_dev == 0 else f" ± {self.abs_dev}")
        if len(self.e_denominators) == 0 and len(self.e_numerators) == 0:
            return out
    
        out += "1" if len(self.e_numerators) == 0 else f"{'*'.join([str(i) for i in self.e_numerators])}"
        out += f"/({'*'.join([str(i) for i in self.e_denominators])})" if len(self.e_denominators) > 0 else ""
        return out

    @property
    def ltx(self):
        # if len(self.f_denominators) > 0:
        #     bl = "\\Bigl("
        #     br = "\\Bigr)"
        # else:
        bl = "("
        br = ")"

        out = f"{bl} {self.ltx_val} \\pm {self.ltx_abs_dev} {br}" if self.abs_dev != 0 else f"{self.ltx_val}"
        if len(self.f_denominators) == 0 and len(self.f_numerators) == 0:
            return out
    
        nums = "1" if len(self.f_numerators) == 0 else f"{' _cdot '.join([str(i) for i in self.f_numerators])}".replace("_cdot", "\\cdot")
        dems = f"{' _cdot '.join([str(i) for i in self.f_denominators])}".replace("_cdot", "\\cdot") 
        
        out += " \\ " + ("\\frac{"+nums+"}{"+dems+"}" if len(self.f_denominators) > 0 else nums)
        return out

    @property
    def rel(self):
        out = f"{self.f_val} ± {self.f_rel_dev}% "
        if len(self.f_denominators) == 0 and len(self.f_numerators) == 0:
            return out

        out += "1" if len(self.f_numerators) == 0 else f"{'*'.join([str(i) for i in self.f_numerators])}"
        out += f"/({'*'.join([str(i) for i in self.f_denominators])})" if len(self.f_denominators) > 0 else ""
        return out

# CALCULATIONS
g = var(9.807, 0, "m", ["s", "s"])

f = var(1/(40*25), 0, "s")                       # 25 fps, 40x slowed

tube_l = var(30, 0.1, "cm", SI=True) 
tube_top_pos = var(792, 1)
tube_bottom_pos = var(976, 1)
tube_h_px = tube_top_pos - tube_bottom_pos
px = tube_l/tube_h_px

base_px = var(1067, 2)
max_px_0 = var(75, 4)
max_px_1 = var(560, 4)
h_0 = base_px - max_px_0
h_1 = base_px - max_px_1

_e = (h_1 / h_0)
e = var.define_by_relative_deviation(
    math.sqrt(_e.val),
    _e.rel_dev / 2)

sampling_speed = var(50000, 0, "samples", "s")
t_half_samp = var(920, 20, "samples")
t_half = t_half_samp / sampling_speed

f_R = var(15300, 100, "Hz")
n = var(1, SI=True) * f_R * t_half

Q_0 = var(2*math.pi) / (var(3/4)/n)

def auto_insert(template, output, *vars):
    template_f = open(template, "r", encoding="utf8")
    in_txt = template_f.read()
    template_f.close()

    for i in range(len(vars)):
        in_txt = in_txt.replace("@" + str(i) + "@", vars[i].ltx)

    # print(in_txt)

    f = open(output, "w", encoding="utf8")
    f.write(in_txt)
    f.close()

auto_insert("info.md", "final.md", 
            e,
            t_half_samp, t_half, 
            f_R, n,
            Q_0)
