""" These initial values are used by all the thermoacoustics animations.
"""

from numpy import pi

refreshRate = 25.0 # Hz  I had this at 15 Hz for a while, which is decent.
period = 5.0 # later I should change back to 10.0 # sec ?
counterMax = int(1.1* refreshRate*period)
wt=0.0
coswt = 0.0;  sinwt = 0.0
dwt = 2*pi/period/refreshRate
firstTime = True
vtogl = False
dtogl = False
zooming = False
purple = (0.6, 0.0, 1.0) #RGB
pink = (0.9, 0.3, 0.7)
darkgreen = (0.0, 0.5, 0.0)
lightgreen = (0.5, 1.0, 0.45)
lightblue = (0.1, 0.5, 1.0)
faint = (0.5, 0.5, 0.5) # for vert lines in ellipse tracing
rad = 0.03 # for thickness of curves, to prevent Moire on projectors having
#            digital keystone correction.  This is not big enough for "big" anims
radBig = 0.1
