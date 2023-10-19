""" Standing-wave thermoacoustics animation, including its options,
   as described in Greg's thermoacoustics book.
Usage when typing in cmd:  'standing.py' or 'standing.py /opt' where opt can be [c,e,k,m,r].
This can also be called from a master.py, by typing 'master.py standing' or 'master.py standing-opt'
Note that renaming this "laser" or "demo", or   'standing.py /l' or 'standing.py /d',
   makes it open with quarter-wave resonator, which Steve Garrett finds useful.
"""
from animTools import *  #which imports everything from visual.

def myWrap(option):
    from inits import refreshRate, period, counterMax, wt, coswt, sinwt, dwt, \
         firstTime, vtogl, dtogl, zooming, \
         purple, pink, darkgreen, lightgreen, lightblue, faint, rad, radBig
    longtitle='Standing-wave thermoacoustic engine or refrigerator animation'
    whowhen='Quickbasic by GWS, 6/1994. Rev python by WCW & GWS, 2010-2015.'
    xcenNorm = -0.5 
    ycenNorm = 5 
    rangeNorm = 10.5

    dxcen = -0.04
    dycen = -0.23
    drange = -0.1

    xcenClose = -1.7
    ycenClose = -1.9
    rangeClose = 7.5

    banner(longtitle,whowhen) # Show disclaimer in output window, then
    #                           start graphical display:
    scene=Display(title=longtitle, center=(xcenNorm,ycenNorm),
                  range=rangeNorm, userzoom=False, userspin=False)
        
    # Initial values of variables that are common to most or all animations are
    #   set in AnimTools.

    # More initial values
    pisi = pi/16
    myCounter = 0
    
    mainName = caller()[0]
    if __name__ == '__main__':  option = caller()[1] 
    if mainName.lower() in ['demo','laser']: option = 'd'
    if option == 'l': option = 'd'  # 'ell' might be misread as 'one'

    if option.lower() =='c':
        phase = 0.
    elif option.lower() == 'e':
        phase = -0.14
    elif option.lower() == 'k': ## Tek dual engine option for book.
        option = 'k'
        phase = 0.
        er = 1
    elif option.lower() == 'm':
        option = 'm'
        phase = 0.07
    elif option.lower() == 'r':
        phase = 0.07
    else: # especially, option really == 'none', which wakes up with "flat" temperature gradient
        if option != 'd': option = 'none'
        lab0 = Label(pos=(0,6), text='Type q to quit.')
        lab1 = Label(pos=(0,5),
            text='Hit any other key repeatedly, to sequence through a series of scenes.')
        lab2 = Label(pos=(0,4),
            text='Later, type first letter:  flat, refrigerator, critical, engine, quit;')
        lab3 = Label(pos=(0,3),
            text='or F for Faster, S for Slower.')
        km = scene.kb.getkey()
        if km.lower() == 'q':  wiseExit( __name__ , scene);  return
        lab0.visible = lab1.visible = lab2.visible = lab3.visible = 0
        phase = 0.14
        er = 1

    hardware=Frame()
    resoleft  = box(pos=(-8.125,2,0), length=0.25, height=2.5, width=0., frame=hardware)
    if option == 'd':
        resobottm = box(pos=(-3.875,0.875), length=8.25, height=0.25, width=0., frame=hardware)
        resotop   = box(pos=(-3.875,3.125), length=8.25, height=0.25, width=0., frame=hardware)
    elif option == 'k':
        resobottm = box(pos=(0.,0.875), length=16, height=0.25, width=0., frame=hardware)
        resotop1   = box(pos=(-6.,3.125), length=4, height=0.25, width=0., frame=hardware)
        resotop2   = box(pos=(3.0,3.125), length=10, height=0.25, width=0., frame=hardware)
        resoright  = box(pos=(8.125,2,0), length=0.25, height=2.5, width=0., frame=hardware)
        vertL = box(pos=(-4,3.75), length=0.25, height=1.5, width=0., frame=hardware)
        vertR = box(pos=(-2,3.75), length=0.25, height=1.5, width=0., frame=hardware)
    else:
        resobottm = box(pos=(0.25,0.875), length=16.5, height=0.25, width=0., frame=hardware)
        resotop   = box(pos=(0.25,3.125), length=16.5, height=0.25, width=0., frame=hardware)
        piston = box(x=8.5,y=2, length=1, height=1.9, width=0., color=color.green, frame=hardware)

    # Initialize pressure and velocity curves and axes, and xi sheets, starting at the top.
    if option == 'd':
        xisheets = xplanes((-7.,0.), height=2, y=2 ) # step is 1 here because xplanes does integer arith here!
        xisheets.shape = lambda o,coswt,sinwt: o.x0 + cos(pi*o.x0/16)*coswt - 0.1*(o.x0+8)/16*sinwt
        xmax = 0.125
    else:
        xisheets = xplanes((-7,7), height=2, y=2 ) # step is 1 here because xplanes does integer arith here!
        xisheets.shape = lambda o,coswt,sinwt: o.x0 + cos(pi*o.x0/16)*coswt - 0.1*(o.x0+8)/16*sinwt
        if option == 'k':
            xmax = 8.
        else:
            xmax = 8.25
    pressure = hplot((-8,xmax),(0,2),text='pressure',y=5) #pressure is a frame
    pressure.shape = lambda o,coswt,sinwt: 1 + .5 * sin(pi*o.x/16.)*coswt #pressure function; o is curve object
    pressure.label.pos += (0.45,0.8)
    velocity = hplot((-8,xmax),(-1,1),text='velocity',y=8.5 )
    if option == 'k':
        velocity.shape = lambda o,coswt,sinwt: -cos(pi * o.x / 16.) * sinwt 
    else:
        velocity.shape = lambda o,coswt,sinwt: -cos(pi * o.x / 16.) * sinwt - (o.x + 8)/16. * .05 * coswt
    velocity.label.pos += (0.45,0.8)

    Stack = Frame()
    yplates = arange(1.2, 2.9, 0.2)
    for y in yplates:
        box(pos=(-5,y,0), length=2, height=1.2*rad, width=0, frame=Stack)
        if option == 'k': 
            box(pos=(5,y,0), length=2, height=1.2*rad, width=0, frame=Stack)
    Stack.show(False)

    magPlate1 = box(pos=(-6.5,-0.2,0), length=7, height=0.2, width=0, visible=0)
    magPlate2 = box(pos=(-6.5,-2.4,0), length=7, height=0.2, width=0, visible=0)

    # yellow oval:
    circle = curve(color=color.yellow, radius=rad/2, visible=0)
    xcen = -5.0;  ycen = 1.3
    xrad = 0.7;  yrad = 0.2
    for i in arange(0, 2*pi+pi/24, pi/24):
        circle.append(pos=(xcen+xrad*cos(i), ycen+yrad*sin(i)))
    if option == 'c' or option == 'e' or option == 'm' or option == 'r': circle.visible = 1

    # moving blob
    smallBlob = box(pos=(-5,ycen,rad), length=0.1, height=0.1, width=0, 
        color = color.cyan, visible=0)
    bigBlob = box(pos=(-5,-1.3), length=0.5, height=1, width=0, 
        color = color.cyan, visible=0)


    # Closup graphs
    PV = Frame(y = -1)
    curve(pos=[(0.0,0.6), (0.0,-1.8), (5,-1.8)], radius=rad, frame=PV) # p-V axes
    Label(pos=(0,1), text='Pressure', frame=PV)
    Label(pos=(2,-2.15), text='Volume of parcel', frame=PV)
    pvsphere = sphere(radius=radBig/2, color=color.cyan, frame=PV)
    ovalP = curve(pos=nullPos, frame=PV, radius=rad/1.35, color=color.cyan)
    fillP = convex(pos=nullPos, frame=PV)
    if option in ['none','m','d']:
        steveMenu1 = Label(pos=(0.5,-5.5), frame=PV,
                text='Choices:  (f)lat, (r)efrigerator, (c)ritical, (e)ngine, (q)uit.')
    if option in ['none','d']:
        steveMenu2 = Label(pos=(0.5,-6), frame=PV,
                text='Now showing: (f)lat.')
    elif option == 'm':
        steveMenu2 = Label(pos=(1.5,-6), frame=PV,
                text='Now showing: (r)efrigerator.')
    PV.show(False)

    TX = Frame(y = -2)
    curve(pos=[(-8.875,-1.3), (-8.875,-3.3), (-3.125,-3.3)], radius=rad, frame=TX) # T-x axes
    Label(pos=(-8,-1), text='Temperature', frame=TX)
    Label(pos=(-6,-3.6), text='Location of parcel', frame=TX)
    txsol = curve(radius=rad/2, frame=TX) # T vs x in the solid
    txsphere = sphere(radius=radBig/2, color=color.cyan, frame=TX)
    ovalT = curve(pos=nullPos, frame=TX, radius=rad/1.35, color=color.cyan)
    topHeatArrow = arrow(length=0.5,  
        headlength=0.3, fixedwidth=1, color=color.red, frame=TX)
    botHeatArrow = arrow(length=0.5, 
        headlength=0.3, fixedwidth=1, color=color.red, frame=TX)
    TX.show(False)

    if option.lower() in ['c', 'e', 'r', 'm']: 
        er = 7
        scene.center = (xcenClose,ycenClose)
        scene.range = rangeClose
        Stack.show(True)
        pressure.show(False);  velocity.show(False)
        magPlate1.visible = magPlate2.visible = 1
        smallBlob.visible = bigBlob.visible = 1
        PV.show(True) 
        txsol.pos=[(-8.875, -2.5 - 4.286*(phase-0.14)), 
                (-3.125,-2.5 + 4.286*(phase-0.14))]
    if option == 'k': Stack.show(True)

    # Calculate and animate everything; only control visibility as the sequence unfolds
    while 1:
        rate(refreshRate) # Pause here, limiting frame update rate to "refreshRate." 
        wt += dwt
        coswt = cos(wt)
        sinwt = sin(wt)
        
        if option not in ['k','d']: 
            piston.x = 8.5 - 0.1*sinwt
        pressure.animate(coswt,sinwt);  velocity.animate(coswt,sinwt)
        xisheets.animate(coswt,sinwt)

        # closup calcs:
        smallBlob.x = -5 + 0.5555702*coswt - 0.040625*sinwt
        bigBlob.x = 4.5*smallBlob.x + 16.5
        aspect = 1 + 0.3*coswt
        smallBlob.length = aspect/10
        bigBlob.length = aspect

        temp = -.3 * cos(wt + 2.5*phase + 0.073)
        locus = 1.5 * coswt
        pvx = 2.5 + cos(wt-phase)
        pvy = -0.8*coswt - 0.5
        pvsphere.x = pvx;  pvsphere.y = pvy
        tx = bigBlob.x
        ty = 1.743934*temp - 2.5
        txsphere.x = tx;  txsphere.y = ty

        # Now decide what should be visible.  Some redundancy here, as it does this every "while"
        #  show() works for Bill's Frames, and visible works for raw vpython objects.
        if er == 1: # resonator, pressure, velocity, and smoke
            pass # pressure.show(True);  velocity.show(True)
        elif er == 2: # add stack
            Stack.show(True)
        elif er == 3: # add yellow circles and zoom in
            circle.visible = 1
        elif er == 4: 
    #        hardware.show(False)
            pressure.show(False);  velocity.show(False)
            magPlate1.visible = magPlate2.visible = 1
            if myCounter < 30:
                myCounter += 1
                scene.center = scene.center + (dxcen, dycen)
                scene.range = scene.range.x + drange
            elif myCounter == 30:
                er += 1
        elif er == 5: # now show the closeup's parcel
            smallBlob.visible = bigBlob.visible = 1
        elif er == 6: # now show the PV graph
            PV.show(True)      # details below in "6 or 7"
        elif er == 7: # now show the T-x graph and heat arrows
            TX.show(True)
            if len(ovalT.pos) < counterMax:
                ovalT.append(pos=(tx, ty, 0.01))
            elif len(ovalT.pos) == counterMax:
                ovalT.append(pos=(tx, ty, 0.01)) # to increment the counter so this doesn't trip again and again        
            shaftWidth = temp - locus * 1.49 * (phase - .14)
            if shaftWidth < 0:
                topHeatArrow.y = 1.7
                topHeatArrow.axis = (0,-1,0)
                botHeatArrow.y = -0.3
                botHeatArrow.axis = (0, 1,0)
            else:
                topHeatArrow.y = 1.2
                topHeatArrow.axis = (0, 1,0)
                botHeatArrow.y = 0.2
                botHeatArrow.axis = (0,-1,0)
            topHeatArrow.x = botHeatArrow.x = bigBlob.x
            topHeatArrow.shaftwidth = botHeatArrow.shaftwidth = abs(shaftWidth)
            topHeatArrow.length = botHeatArrow.length = 0.5
            topHeatArrow.visible = botHeatArrow.visible = (phase != 0.0) #stops flicker at gradTcrit
        else: # exit! if er = 8
           wiseExit( __name__ , scene)
           return
        if er == 6 or er == 7: # pv ellipse
            if len(ovalP.pos) < counterMax:
                ovalP.append(pos=(pvx, pvy, 0.01))
            elif len(ovalP.pos) == counterMax:
                if phase != 0.0: fillP.pos = ovalP.pos
                if phase == -0.14: 
                    fillP.color = darkgreen
                elif phase == 0.07 or phase == 0.14:
                    fillP.color = lightgreen
                ovalP.append(pos=(pvx, pvy, 0.01)) # to increment the counter so this doesn't trip again and again                

        if scene.kb.keys:  
            key = scene.kb.getkey()
            if key.lower() == 'q' or option in ['c','e','k','r']:
                wiseExit( __name__ , scene)
                return
            phaseOld = phase

            if key == 'F':  
                dwt *= 2;  counterMax //= 2.
            elif key.upper() == 'S':  
                dwt /= 2;  counterMax *= 2.
            elif key == 'f':  
                phase = 0.14
                steveMenu2.text='Now showing: (f)lat.'
                if er < 7: er += 1
            elif key.lower() == 'r':  
                phase = 0.07
                steveMenu2.text='Now showing: (r)efrigerator.'
                if er < 7: er += 1
            elif key.lower() == 'c':  
                phase = 0.0
                steveMenu2.text='Now showing: (c)ritical.'
                if er < 7: er += 1
            elif key.lower() == 'e':  
                phase = -0.14
                steveMenu2.text='Now showing: (e)ngine.'
                if er < 7: er += 1 
            else:
                if er < 7: er += 1
            txsol.pos=[(-8.875, -2.5 - 4.286*(phase-0.14), 0), 
                (-3.125,-2.5 + 4.286*(phase-0.14),0)] #necessary only for f,r,c,e, but no harm done otherwise

            if er == 7 and len(ovalT.pos) != 0: 
                ovalT.pos = ovalP.pos = fillP.pos = []
            if er == 7 and len(ovalP.pos) != 0 and phase != phaseOld: #User has changed phase at inappropriate time.
                ovalP.pos = fillP.pos = []
#    end of definition of myWrap function

if __name__ == "__main__":
    myWrap('dummy')

