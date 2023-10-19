""" This is thermal penetration depth animation,
as described in Greg's thermoacoustics book.
Usage when typing in cmd:  'thermal.py' or 'thermal.py /opt' where opt can be [e,w,y].
This can also be called from a master.py, by typing 'master.py thermal' or 'master.py thermal-opt'.
"""
from animTools import *  #which imports everything from visual.

def myWrap(option):
    from inits import refreshRate, period, wt, coswt, sinwt, dwt, \
         firstTime, vtogl, dtogl, zooming, \
         purple, pink, darkgreen, lightgreen, lightblue, faint, rad, radBig
    longtitle='Thermal Penetration Depth Animation'
    whowhen='Quickbasic by GWS, 6/1994. Rev python by WCW & GWS, 2010-2015.'
    xcenNorm = -0.5 
    ycenNorm = 5 
    rangeNorm = 10.5

    banner(longtitle,whowhen) # Show disclaimer in output window, then
    #                           start graphical display:
    scene=Display(title=longtitle, center=(xcenNorm,ycenNorm), range=rangeNorm,
        autoscale = 0, userzoom=False, userspin=False)

    # Initial values of variables that are common to most or all animations are
    #   set in AnimTools.

    # More initial values
    pisi = pi/16
    key = 'none'

    offset2 = 0.

    if __name__ == '__main__':  option = caller()[1] 

    if option == 'none':
        lab1 = Label(pos=(0,5),
            text='Hit any key, repeatedly, to sequence through a series of scenes.')
        lab2 = Label(pos=(0,4),
            text='The q key will quit the animation.')
        km = scene.kb.getkey()
        if km.lower() == 'q':  wiseExit( __name__ , scene);  return
        lab1.visible = lab2.visible = 0

    hardware=Frame()
    resobottm = box(pos=(0.25,0.875), length=16.5, height=0.25, width=0., frame=hardware)
    resotop   = box(pos=(0.25,3.125), length=16.5, height=0.25, width=0., frame=hardware)
    resoleft  = box(pos=(-8.125,2,0), length=0.25, height=2.5, width=0., frame=hardware)
    piston = box(x=8.5,y=2, length=1, height=1.9, width=0., color=color.green, frame=hardware)

    # Initialize main-scene curves and axes, and xi sheets, starting at the top.
    pressure = hplot((-8,8.25),(0,2),text='pressure',y=5) #pressure is a frame
    pressure.shape = lambda o,coswt,sinwt: 1 + .5 * sin(pi * o.x / 16.) * coswt #pressure function; o is curve object
    pressure.label.pos += (0.45,0.8)
    temperature = hplot((-8,8.25),(0,2),text='temperature',y=8.5) #pressure is a frame
    temperature.shape = lambda o,coswt,sinwt: 1 + .2 * sin(pi * o.x / 16.) * coswt #pressure function; o is curve object
    temperature.label.pos += (2,1.4)
    velocity = hplot((-8,8.25),(-1,1),text='velocity',y=8.5 )
    velocity.shape = lambda o,coswt,sinwt: -cos(pi * o.x / 16.) * sinwt - (o.x + 8)/16. * .05 * coswt
    velocity.label.pos += (0.45,0.8)
    xisheets = xplanes((-7,7), height=2, y=2 )
    xisheets.shape = lambda o,coswt,sinwt: o.x0 + cos(pi*o.x0/16)*coswt - 0.1*(o.x0+8)/16*sinwt
    temperature.show(False)
    if option != 'w': menu = Label(pos=(-0.5,-0.5),text='Type "F" for faster, "S" for slower, or any other key to change scene.')

    # three circles:
    topcircle = curve(color=color.yellow, radius=rad, visible=0)
    for pt in arc(-7.7, 9.5, 1, 0, 360): topcircle.append(pos=pt)
    midcircle = curve(color=color.yellow, radius=rad, visible=0)
    for pt in arc(-7.7, 6, 1, 0, 360): midcircle.append(pos=pt)
    botcircle = curve(color=color.yellow, radius=rad, visible=0)
    for pt in arc(-7.7, 2, 1, 0, 360): botcircle.append(pos=pt)

    # Initialize the boundary-layer scene:
    BL = Frame()
    rottline = hplot((0.,7.),(-1.2,1.2),text='temperature',tics=6, x=1., y=7.8, points=40, radius=rad/1.5, frame=BL)
    rottline.shape = lambda o, coswt,wt: coswt - exp(-o.x)*cos(wt-o.x)
    rottline.label.pos += (0.2,1.0)
    pressurecloseup = hplot((0.,7.),(-1.0,1.0),text='pressure', x=1., y=5., points=2, radius=rad/1.5, frame=BL)
    pressurecloseup.shape = lambda o,coswt,sinwt: coswt
    pressurecloseup.label.pos += (0.1,0.8)
    ticmarks = [];  lengthtics = 0.15 # make tics on horiz pressure axis:
    for xx in range (1,7):  ticmarks.append(curve(frame=BL, radius=rad/1.5,
        pos=[(1+xx,5-lengthtics/2),(1+xx,5+lengthtics/2)]))
    clupsheets = xplanes((1.,9.), height=2., x=1., y=5., planes=9, frame=BL)
    clupsheets.shape = lambda o,coswt,wt: o.x0 - 0.15*o.x0*coswt + 0.0707*(exp(-o.x0)*cos(wt-pi/4-o.x0) - cos(wt-pi/4))
    Label(text='y/dk',pos=(8.5,7.6), frame=BL)
    BL.show(False)

    tp = 6.;  bt = 4.
    BLpiston = curve(radius=rad, color=color.green, visible=0,
        pos=[(0,bt),(0,bt),(0,tp),(0,tp),(0,bt),])

    BLoval = Frame()
    ovalcurve = curve(pos=nullPos, frame=BLoval, radius=0.65*rad)
    ovalfill = convex(pos=nullPos, color=purple, frame=BLoval)
    marker = sphere(frame=BLoval, radius=2*rad, color=color.yellow)
    BLoval.show(False)

    Wx = Frame(x=1.0,y=2.5) # plot of W(y) vs y
    wx = curve(pos=nullPos, radius=rad/1.5, frame=Wx)
    for x in arange(0.0, 7.1, 0.1):
      y = 1 - exp(-x)*(sin(x) + cos(x))
      wx.append(pos=(x, y))
    curve(pos=[(7,0),(0,0),(0,1)], radius=rad/1.5, frame=Wx) #axes
    tics2 = [] # make tics on horiz axis:
    for xx in range (1,7):  tics2.append(curve(frame=Wx, radius=rad/1.5,
        pos=[(xx, -lengthtics/2), (xx, lengthtics/2)]))
    Label(text='Loop area',pos=(-1.5, 1), frame=Wx)
    Label(text='(= work done',pos=(-1.5, 0.5), frame=Wx)
    Label(text='by piston)',pos=(-1.5, 0), frame=Wx)
    Wx.show(False)

    dWx = Frame(x=1.0,y=1) # plot of W(y) vs y
    dwx = curve(pos=nullPos, radius=rad/1.5, frame=dWx)
    for x in arange(0.0, 7.1, 0.1):
      y = 4*exp(-x)*sin(x)
      dwx.append(pos=(x, y))
    curve(pos=[(7,0),(0,0)], radius=rad/1.5, frame=dWx) #axes
    curve(pos=[(0,-0.5),(0,1)], radius=rad/1.5, frame=dWx) #axes
    tics3 = [] # make tics on horiz axis:
    for xx in range (1,7):  tics2.append(curve(frame=dWx, radius=rad/1.5,
        pos=[(xx, -lengthtics/2), (xx, lengthtics/2)]))
    Label(text='dW/dy',pos=(-1, 0.6), frame=dWx)
    dWx.show(False)

    quitHint = Frame(x=3,y=1)
    Label(text='Type q',pos=(5.7, 0.6), frame=quitHint)
    Label(text='to quit.',pos=(6.0, 0.25), frame=quitHint)
    quitHint.show(False)

    # book options for this animation were e, w, and y.
    if option == 'e':
        viewcounter = 9 # essentially 6, but this makes oval trace work
        hardware.show(False)
        pressure.show(False);  velocity.show(False)
        xisheets.show(False)
        menu.visible = 0
        scene.center = (3.8, 4.7);  scene.range = 6.5
        BL.show(True)
        BLpiston.visible = 1
        Wx.show(True)
        whenOvalBegan = wt
    elif option == 'w':
        viewcounter = 1
    elif option == 'y':
        viewcounter = 5
    else:
        viewcounter = 0
        option = 'none' # catch a typo;  treat as 'none'


    # Calculate and animate everything; only control visibility as the sequence unfolds
    while 1:
        rate(refreshRate) # Pause here, limiting frame update rate to "refreshRate." 
        wt += dwt
        coswt = cos(wt)
        sinwt = sin(wt)
        
        piston.x = 8.5 - 0.1*sinwt
        if viewcounter < 5:
            pressure.animate(coswt,sinwt);  velocity.animate(coswt,sinwt)
            temperature.animate(coswt,sinwt)
            xisheets.animate(coswt,sinwt)
        else:
            pressurecloseup.animate(coswt,sinwt)
            rottline.animate(coswt,wt)
            clupsheets.animate(coswt,wt)

        xf = 4  # 4, for the smoke at 4dk.  +1 for frame offset, +0.25 for piston thickness
        xp = 1. + xf - 0.15*xf*coswt + 0.0707*(exp(-xf)*cos(wt-pi/4-xf) - cos(wt-pi/4))
        BLpiston.x[0] = BLpiston.x[3] = BLpiston.x[4] = xp
        BLpiston.x[1] = BLpiston.x[2] = xp + 0.25    
        marker.x = xp
        marker.y = 5 + coswt
        
        if scene.kb.keys:  
            if option != 'none':
                wiseExit( __name__ , scene)
                return
            key = scene.kb.getkey()
            if key.upper() == 'F' and viewcounter <= 10:  
                dwt *= 2
            elif key.upper() == 'S' and viewcounter <= 10:  
                dwt /= 2
            elif key.lower() == 'q':
                wiseExit( __name__ , scene);  return
            else:
                viewcounter += 1

        # Now decide what should be visible.
        #  show() works for Bill's Frames, and visible works for raw vpython objects.
        if viewcounter == 0: # only the reso and piston, smoke, v, and p graphs
            pass
        elif viewcounter == 1: # get rid of v, add T graph
            temperature.show(True);  velocity.show(False)
            viewcounter += 1
        elif viewcounter == 3: # add yellow circles
            for i in [topcircle,midcircle,botcircle]: i.visible = 1
            viewcounter += 1
        elif viewcounter == 5: # start BL view, with T and P
            hardware.show(False)
            pressure.show(False);  velocity.show(False);  temperature.show(False)
            xisheets.show(False)
            for i in [topcircle,midcircle,botcircle]: i.visible = 0
            menu.visible = 0
            scene.center = (3.8, 4.7)
            scene.range = 6.5
            BL.show(True)
            viewcounter += 1
        elif viewcounter == 7: # add piston
            BLpiston.visible = 1
            viewcounter += 1        
        elif viewcounter == 9: # add pV ellipse
            BLoval.show(True)
            whenOvalBegan = wt
            viewcounter += 1
        elif viewcounter >= 10:
            if wt - whenOvalBegan < 6.9:
                ovalcurve.append(pos=(marker.x, marker.y, 0.01))
            elif ovalfill.pos.any() != ovalcurve.pos.any():
                ovalfill.pos = ovalcurve.pos
        if viewcounter == 11: # add loop area vs y
            Wx.show(True)
            viewcounter += 1
        elif viewcounter == 13: # add dW/dy vs y
            dWx.show(True)
            viewcounter += 1
        elif viewcounter == 15:
            quitHint.show(True)
#    end of definition of myWrap function

if __name__ == "__main__":
    myWrap('dummy')
