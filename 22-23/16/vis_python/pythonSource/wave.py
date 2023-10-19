""" Animation of traveling wave, standing wave, or anything inbetween,
as described in Greg's thermoacoustics book.
Usage when typing in cmd:  'wave.py' or 'wave.py /opt' where opt can be [k,s,t,u,v].
This can also be called from a master.py, by typing 'master.py wave' or 'master.py wave-opt'.
"""

from animTools import *  #which imports everything from visual, which in turn imports numpy.

def myWrap(option):
    from inits import refreshRate, period, wt, coswt, sinwt, dwt, \
         firstTime, vtogl, dtogl, zooming, \
         purple, pink, darkgreen, lightgreen, lightblue, faint, rad, radBig
    longtitle='Traveling - Standing Wave Animation'
    whowhen='Quickbasic by GWS, 10/1998. Rev python by WCW & GWS, 2010-2015.'
    xcenNorm = -1.
    ycenNorm = 4.5
    rangeNorm = 11

    banner(longtitle,whowhen) # Show disclaimer in output window, then
    #                           start graphical display:
    scene=Display(title=longtitle, center=(xcenNorm,999),
                  range=rangeNorm, userzoom=False, userspin=False)
    # Center will be redefined after initializations, at firstTime test.

    # More initial values
    pisi = pi/16
    key = 'none'

    if __name__ == '__main__': option = caller()[1]  # otherwise use option passed from master.
    #  Book options were k, s, t, u, v
    if option == 'none' or option == 't':
        right = 1.0;  
    elif option == 's':
        right = 0.5
    elif option == 'u':
        right = 0.5;  vtogl = 1;  whenBeganOval = wt
    elif option == 'v':
        right = 1.0;  vtogl = 1;  whenBeganOval = wt   
    elif option == 'k':
        right = 0.53;  vtogl = 1;  whenBeganOval = wt
    else: 
        right = 1.0
        option = 'none'

    if option == 't':
        s = 'p(x,t) = constant + A cos(wt - kx)'
    elif option == 's':
        s = "p(x,t) = constant + A cos(wt - kx) +  A cos(wt + kx)"
    else:
        s1 = 'p(x,t) = constant + R cos(wt - kx) + (1 - R) cos(wt + kx).      R = '
        s = s1 + str(right)
    lab1 = Label(pos=(-1,0), text=s)
    if option == 'none':
        lab2 = Label(pos=(-1,-1), 
            text="Typing c changes R, v toggles pV diagrams on/off, F faster, S slower, q quits.")

    # pressure graph
    p = curve(radius=rad)
    for i in range(24):
        p.append(pos=(i-12,1, 0.03),color=color.cyan)
    curve(pos=[(-11.05, 6.92), (10.2, 6.92)],radius=rad) # x axis
    curve(pos=[(-11.05, 6.92), (-11.05, 9.2)],radius=rad)  # y axis
    curve(pos=[(-11.0, 8.5), (10.4, 8.5)]) # pm line
    Label(pos=(-9.8, 9), text="pressure")
    Label(pos=(-11.5, 8.5), text="pm")
    Label(pos=(-11.35, 6.92), text="0")
    # from visual.text import *, and then text also works (for upper case only)

    # velocity graph
    v = curve(radius=rad)
    for i in range(24):
        v.append(pos=(i-12, 1), color=color.cyan)
    curve(pos=[(-11.05, 4.92), (10.4, 4.92)], radius=rad) # x axis
    curve(pos=[(-11.05, 6.12),(-11.05, 3.72)], radius=rad)  # y axis
    Label(pos=(-9.9, 6), text="velocity")
    Label(pos=(-11.4, 4.92), text="0")

    # Draw the box and smoke lines.
    box(pos=(-1, 0.75), length=22, height=0.5, width=0,)
    box(pos=(-1, 3.25), length=22, height=0.5, width=0,)
    smoke = []
    for i in range(24): 
        smoke.append(curve(pos=[(0,1,-0.02),(0,3,-0.02)],color=color.cyan, radius=rad))

    # pv ellipses:
    # Start to draw both when vtogl is tripped.
    # Null them all when vtogl is turned off or R is changed.
    # Therefore, calculate pbottom, xbuf, etc even if they are not displayed.
    Ovals = Frame()
    ovalLeft = curve(frame=Ovals, radius=rad/2)
    fillLeft = convex(frame=Ovals)
    vertLineLeft = curve(pos=[(-5, 3.2, 0.02),(-5, 8.5, 0.02)], color=faint, radius=rad, frame=Ovals)
    horLineLeft = curve(pos=[(-5, 3.2, 0.02),(-5, 8.5, 0.02)], color=faint, radius=rad, frame=Ovals)
    ovalRight = curve(frame=Ovals, radius=rad/2)
    fillRight = convex(frame=Ovals)
    vertLineRight = curve(pos=[(2, 3.2, 0.02),(2, 8.5, 0.02)],color=faint, radius=rad, frame=Ovals)
    horLineRight = curve(pos=[(2, 3.2, 0.02),(2, 8.5, 0.02)], color=faint, radius=rad, frame=Ovals)
    if not vtogl: Ovals.show(False)

    # Animate
    while 1:
        rate(refreshRate) # Pause here, limiting frame update rate to "refreshRate." 
        wt += dwt
        sinwt = sin(wt)
        coswt = cos(wt)
        trmo = 2. * right - 1
        
        for j in range(24): 
            coskx = cos(pisi*j)
            sinkx = sin(pisi*j)
            p.y[j]= 8.5 + 0.5*(coskx*coswt + trmo*sinkx*sinwt)
            v.y[j] = 4.92 + sinkx*sinwt + trmo*coskx*coswt
            for i in [0,1]: 
                smoke[j].x[i] = j -12 - sinkx*coswt + trmo*coskx*sinwt
        if vtogl:
            for i in [0,1]:
                vertLineLeft.x[i] = smoke[7].x[0]
                vertLineRight.x[i] = smoke[14].x[0]
            vertLineLeft.y[1] = p.y[7]
            vertLineRight.y[1] = p.y[14]
            horLineLeft.x[0] = vertLineLeft.x[1]
            horLineRight.x[0] = vertLineRight.x[1]
            for i in [0,1]:
                horLineLeft.y[i] = vertLineLeft.y[1]
                horLineRight.y[i] = vertLineRight.y[1]
            if wt - whenBeganOval < 6.9: 
                ovalLeft.append(pos=(smoke[7].x[0], p.y[7], 0.01))
                ovalRight.append(pos=(smoke[14].x[0], p.y[14], 0.01))
            elif fillLeft.pos.any() != ovalLeft.pos.any(): # if time>2pi and not yet filled:
                fillLeft.pos = ovalLeft.pos
                fillRight.pos = ovalRight.pos
                if right > 0.5:
                    fillLeft.color = purple
                    fillRight.color = purple
                else:
                    fillLeft.color = pink
                    fillRight.color = pink

    # Now decide what should be visible.
    #  show() works for Bill's Frames, and visible works for raw vpython objects.
        if scene.kb.keys:  
            if option != 'none':
                wiseExit( __name__ , scene)
                return
            key = scene.kb.getkey()
            if key.lower() == 'v':
                vtogl = not vtogl
                if vtogl: #vtogl has just been changed to True:
                    Ovals.show(True)
                    whenBeganOval = wt
                else: # vtogl has just been changed to False: 
                    Ovals.show(False)
                    ovalLeft.pos=nullPos;  fillLeft.pos=nullPos
                    ovalRight.pos=nullPos;  fillRight.pos=nullPos
            elif key.lower() == 'c': 
                lab1.text = s1
                lab2.visible = 0
                s = ''
                kc = ''
                while kc != '\n':
                    s += kc
                    kc = scene.kb.getkey()
                    lab1.text = s1 + s + kc
                try:
                    right = float(s)
                    right = max(right,0);  right = min(right,1)
                    lab1.text = s1 + str(right)
                except:
                    pass
                lab2.visible = 1
                ovalLeft.pos=nullPos;  fillLeft.pos=nullPos
                ovalRight.pos=nullPos;  fillRight.pos=nullPos
                whenBeganOval = wt
            elif key.upper() == 'F':  
                dwt *= 2
            elif key.upper() == 'S':  
                dwt /= 2
            elif key.lower() == 'q':
                wiseExit( __name__ , scene)
                return
            else: pass
        if firstTime: 
            firstTime=False
            scene.center = (xcenNorm, ycenNorm)
#    end of definition of myWrap function

if __name__ == "__main__":
    myWrap('dummy')

