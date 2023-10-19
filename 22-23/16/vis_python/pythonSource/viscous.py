""" Animation of viscous penetration depth in boundary-layer approximation,
as described in Greg's thermoacoustics book.
Usage when typing in cmd:  'viscous.py' or 'viscous.py /m' .
This can also be called from a master.py,
   by typing 'master.py viscous' or 'master.py viscous-m' .
Renaming it as oscwall.py, oscwall.exe (after py2exe), or typing 'viscous.py /o'
starts it with a boundary-layer closeup with moving wall.
Similarly, 'master.py viscous-o'.  
"""

from animTools import *  #which imports everything from visual.

def myWrap(option):
    from inits import refreshRate, period, counterMax, wt, coswt, sinwt, dwt, \
         firstTime, vtogl, dtogl, zooming, \
         purple, pink, darkgreen, lightgreen, lightblue, faint, rad, radBig
    longtitle='Viscous Penetration Depth Animation'
    whowhen='Quickbasic by GWS, 6/1994. Rev python by WCW & GWS, 2010-2015.'
    xcenNorm = -0.5 
    ycenNorm = 5 
    rangeNorm = 10.5

    banner(longtitle,whowhen) # Show disclaimer in output window, then
    #                           start graphical display:
    scene=Display(title=longtitle, center=(xcenNorm,ycenNorm),
                  range=rangeNorm, userzoom=False, userspin=False)
        
    # Initial values of variables that are common to most or all animations are
    #   set in AnimTools.
    
    # More initial values
    pisi = pi/16
    key = 'none'
    lagrange = False
    offset2 = 0.

    mainName = caller()[0]
    if __name__ == '__main__': option = caller()[1] 

    if option == 'none' and mainName.lower() != 'oscwall':
        lab1 = Label(pos=(0,5),
            text='Hit any key, repeatedly, to sequence through a series of scenes.')
        lab2 = Label(pos=(0,4),
            text='Later, in the boundary-layer scene, "L" controls the frame of reference.')
        lab3 = Label(pos=(0,3),
            text='"q" will terminate the animation.')
        km = scene.kb.getkey()
        if km.lower() == 'q':  wiseExit( __name__ , scene);  return
        lab1.visible = lab2.visible = lab3.visible = 0
    elif mainName.lower() == 'oscwall': 
        lab3 = Label(pos=(0,3),
            text='"q" will terminate the animation.')
        lab3.visible = 0

    hardware=Frame()
    resobottm = box(pos=(0.25,0.875), length=16.5, height=0.25, width=0., frame=hardware)
    resotop   = box(pos=(0.25,3.125), length=16.5, height=0.25, width=0., frame=hardware)
    resoleft  = box(pos=(-8.125,2,0), length=0.25, height=2.5, width=0., frame=hardware)
    piston = box(x=8.5,y=2, length=1, height=1.9, width=0., color=color.green, frame=hardware)

    # Initialize pressure and velocity curves and axes, and xi sheets, starting at the top.
    pressure = hplot((-8,8.25),(0,2),text='pressure',y=5) #pressure is a frame
    pressure.shape = lambda o,coswt,sinwt: 1 + .5 * sin(pi * o.x / 16.) * coswt #pressure function; o is curve object
    pressure.label.pos += (0.45,0.8)
    velocity = hplot((-8,8.25),(-1,1),text='velocity',y=8.5 )
    velocity.shape = lambda o,coswt,sinwt: -cos(pi * o.x / 16.) * sinwt - (o.x + 8)/16. * .05 * coswt
    velocity.label.pos += (0.45,0.8)
    xisheets = xplanes((-7,7), height=2, y=2 ) # step is 1 here because xplanes does integer arith here!
    xisheets.shape = lambda o,coswt,sinwt: o.x0 + cos(pi*o.x0/16)*coswt - 0.1*(o.x0+8)/16*sinwt
    pressure.show(False);  velocity.show(False);  xisheets.show(False)
    menu = Label(pos=(-0.5,-0.5),text='Type "F" for faster, "S" for slower, "q" to quit, or any other key to change scene.')

    # twocircles:
    topcircle = curve(color=color.yellow, radius=rad, visible=0)
    for pt in arc(0,6,1,0,360): topcircle.append(pos=pt)
    botcircle = curve(color=color.yellow, radius=rad, visible=0)
    for pt in arc(0,1,1,0,360): botcircle.append(pos=pt)

    # Initialize the boundary-layer scene:
    BL = Frame()
    pressurecloseup = hplot((-2.,2.),(-.8,.8),text='pressure', y=9.5,points=2, radius=rad/1.5, frame=BL)
    pressurecloseup.shape = lambda o,coswt,sinwt: 0.2*o.x*coswt
    rottline = vplot((-2,2),(0,6.7),text='y/dv',tics=6,y=1.5, points=40, radius=rad/1.5, frame=BL)
    rottline.shape = lambda o, coswt,sinwt: ((1-exp((-1-1j)*o.y))*(1.5*coswt+1.5j*sinwt)).real
    BL.show(False)

    if option == 'm':
        viewcounter = 7
    elif mainName.lower() == 'oscwall' or option == 'o':
        viewcounter = 7
        lagrange = True
        offset = 0
    else:
        viewcounter = 0

    # Calculate and animate everything; only control visibility as the sequence unfolds
    while 1:
        rate(refreshRate) # Pause here, limiting frame update rate to "refreshRate." 
        wt += dwt
        coswt = cos(wt)
        sinwt = sin(wt)
        
        piston.x = 8.5 - 0.1*sinwt

        if lagrange:
            scene.center.x = (1.5*coswt + 1.5j*sinwt).real - offset
            offset2 = scene.center.x # set up for future switch to Eulerian frame of reference
        else:
            scene.center.x = offset2
            offset = (1.5*coswt+1.5j*sinwt).real - offset2 # set up for future switch to Lagrangian frame of reference

        if scene.kb.keys:  
            key = scene.kb.getkey()
            if key.upper() == 'F':  
                dwt *= 2
            elif key.upper() == 'S':  
                dwt /= 2
            elif key.upper() == 'L' and viewcounter == 8:
                lagrange = not lagrange
                pressurecloseup.show(not lagrange)
            elif key.lower() == 'q':
                wiseExit( __name__ , scene);  return
            elif viewcounter < 8:
                viewcounter += 1

        # Now decide what should be visible.
        #  show() works for Bill's Frames, and visible works for raw vpython objects.
        if viewcounter == 0: # only the reso and piston
            pass
        elif viewcounter == 1: # add p and v graphs
            pressure.show(True);  velocity.show(True)
            viewcounter = 2
        elif viewcounter == 2:
            pressure.animate(coswt,sinwt);  velocity.animate(coswt,sinwt)
        elif viewcounter == 3: # add smoke
            xisheets.show(True)
            viewcounter = 4
        elif viewcounter == 4 or viewcounter == 6:
            pressure.animate(coswt,sinwt);  velocity.animate(coswt,sinwt)
            xisheets.animate(coswt,sinwt)
        elif viewcounter == 5: # add yellow circles
            topcircle.visible = botcircle.visible = 1
            viewcounter = 6
        elif viewcounter == 7: # start the BL view
            hardware.show(False)
            pressure.show(False);  velocity.show(False)
            xisheets.show(False)
            topcircle.visible = botcircle.visible = 0
            menu.visible = 0
            scene.pos = (0,0)
            scene.range = 7
            BL.show(True)
            if mainName.lower() == 'oscwall' or option == 'o': pressurecloseup.show(False)
            Label(pos=(0,0.5),text='   Type "F" for faster, "S" for slower, "L" to toggle \nbetween Eulerian and Lagrangian views, "q" to quit.')
            viewcounter = 8
        elif viewcounter == 8:
            pressurecloseup.animate(coswt,sinwt)
            rottline.animate(coswt,sinwt)
#        elif viewcounter >= 9: # exit!
 #           wiseExit( __name__ , scene)
  #          return
#    end of definition of myWrap function

if __name__ == "__main__":
    myWrap('dummy')

