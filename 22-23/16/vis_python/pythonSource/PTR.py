""" Animation of Stirling and pulse-tube refrigerators, as described
in Greg's thermoacoustics book.
Usage when typing in cmd:  'ptr.py' or 'ptr.py /opt' where opt can be [c,p,r,s]
This can also be called from a master.py, by typing 'master.py ptr' or 'master.py ptr-opt'.
Overall structure of this and the other thermoacoustics animations:
First, create objects.
Second, animate them.
Third, test for keyboard input and make necessary changes.
"""
from animTools import *    # which imports everything from visual
from feedbackers import *  # functions shared by tashe and ptr

def myWrap(option):  # Define the entire animation as a function, so it can be opened
                     # by another python or run independently via last two lines.
    from inits import refreshRate, period, wt, coswt, sinwt, dwt, \
         firstTime, vtogl, dtogl, zooming, \
         purple, pink, darkgreen, lightgreen, lightblue, faint, rad, radBig
    longtitle='Pulse Tube Refrigerator Animation'
    whowhen='Quickbasic by GWS, 6/1994. Rev python by WCW & GWS, 2010-15.'
    xcenNorm = 110.
    ycenNorm = -2.0
    rangeNorm = 53.
    xcenReg = 88.5 
    ycenReg = 4.0 
    rangeReg = 5. 
    xcenBuf = 115.5 
    ycenBuf = 4.0 
    rangeBuf = 10. 
    xcenCold = 96.5
    ycenCold = 3
    rangeCold = 3.5

    banner(longtitle,whowhen) # Show disclaimer in output window;  then
    #                           start graphical display:
    # scene=Display(title=longtitle, center=(xcenNorm,200), range=rangeNorm)
    scene=Display(title=longtitle, center=(xcenNorm,200),
                  range=(rangeNorm,0.785*rangeNorm,rangeNorm), userzoom=False, userspin=False)
    # scene=Display(title=longtitle, center=(xcenNorm,200), range=(999,0.785*rangeNorm,999)) disaster.
    # scene=Display(title=longtitle, center=(xcenNorm,200), scale=(1./rangeNorm,1./0.785/rangeNorm,1./rangeNorm))
    # scene=Display(title=longtitle, center=(xcenNorm,200), scale=(1./999,1./0.785/rangeNorm,1./999))

    #Center.y will be redefined at firstTime test.

    if __name__ == '__main__': option = caller()[1]
    #  Book options were c, o, p, r, s  ??
    if option == 'c':
        key = 's'
        dtogl = 1
        vtogl = 1 
    elif option == 'o':
        key = 'o'
    elif option == 'p':
        key = 'O'
        vtogl = 1
    elif option == 'r':
        key = 'r'; myCounter = 31
    elif option == 's':
        key = 's'
        vtogl = 1
        dtogl = 1
    else: # includes "none"
        key = 'none'
        option = 'none'


    # More initial values
    reph = 15.0;  imph = -0.135
    repc = 12.0;  impc = 0.

    rexR = 5*sin(0.026737*130);  imxR = 120./220.
    rexL = 9.25*sin(0.026737*106);   imxL = 96./119.
    rexb = -2.5;  imxb = -1.4
    ##rexinert = (rexL*impc - imxL*repc) * (reph - repc) / (reph*impc - imph*repc)
    ##imxinert = (rexL*impc - imxL*repc) * (imph - impc) / (reph*impc - imph*repc)
    rexinert = -18.7;  imxinert = -0.84580 + 9.25*sin(.026737*110)*coswt + 100./119.*sinwt
    rexr = (7.5 * rexR + 12.5 * rexL) / 20
    imxr = (7.5 * imxR + 12.5 * imxL) / 20
    lab3 = Label(pos=(109.5,-39), text="")
    whenOvalsBegan = whenBufOvalsBegan = whenRegOvalsBegan = whenChxOvalsBegan = wt

    if option == 'none':
        lab1 = Label(pos=(106,200-33), # was 35
            text='Type "m" to always show the menu, or any other key to always suppress it.')
        km = scene.kb.getkey()
        lab1.text = "         Type s, o, O, or f to start animation with"
        lab1.x = 80
        lab2 = Label(pos=(110,200-37), # was 39
            text=" Stirling, optr(with piston), Optr(with no driver), or feedback ptr.")
        key = scene.kb.getkey() #get key to control initial view
        if key.lower() != 'o' and key.lower() != 'f':  key = 's'
        lab1.visible = lab2.visible = 0

        if km.lower() == 'm': 
            lab3.text="stirling, optr, Optr, fptr, regen, coldX, p-tube, v-togl, quit, Faster, Slower"
            if key == 's':
                lab3.text = "stirling, optr, Optr, fptr, regen, coldX, v-togl, d-togl, quit, Faster, Slower"
    else:
        km = 'none'
        lab3.visible = 0
    ks = '0';  oldKey = key

    # functions for things common to tashe and ptr:
    reg, rightHX, ambientArrow, remoteArrow = addHeart() # The Stirling "heart"  ?? see kluge in line 211 of ptr.bas
    for b in rightHX: b.color = color.blue
    # later, for view 'c', I will also have to return the regen, and adjust .x of both in zooming
    # Make other objects visible momentarily, so Frame can make complete lists.
    LeftPist, leftPiston, rightPiston = addPistons() # the pistons
    curve(pos=[(70,14), (77,14)], frame=LeftPist, radius=radBig) # pipe around left piston
    curve(pos=[(70, 4), (77, 4)], frame=LeftPist, radius=radBig)
    rightPiston.color = color.blue
    words = Label(pos=(117,9)) # Words describing piston motion
    ## font='helvetica.bold' or 'times new roman' seems to work in label, too.
    Tbt, Feedback = addPipes() # the tbt and feedback pipes, in two frames.
    Label(pos=(97,16),frame=Feedback,text="-100 C")
    Label(pos=(77,0),frame=Feedback,text="30 C")
    Label(pos=(100,-4),frame=Feedback,text="30 C")
    Label(pos=(138,11.5),frame=Feedback,text="30 C")

    NoPist = Frame()  # Optr needs pipe extension left:
    curve(pos=[(55,14),(77,14)],radius=radBig, frame = NoPist)
    curve(pos=[(55, 4),(77, 4)],radius=radBig, frame = NoPist)

    LRC = Frame()
    curve(pos = [(125,4), (125,7.5), (130,7.5), (130,-2), (145.5, -2), 
        (145.5,20), (130,20), (130,10.5), (125,10.5), (125,14)], 
        radius = radBig, frame = LRC)

    smoke = addSmoke() # smoke lines in regen, tbt, and feedback
    for i in [4,5,6,7,8]:  smoke[i].frame = Tbt
    for i in [9,10,11,12,13,14,15]:  smoke[i].frame = Feedback
    leftSmoke = []  # the smoke lines in 'O' view, left of the normal piston
    for i in range(5):
        leftSmoke.append(curve(pos=[(0,4,-0.2),(0,14,-0.2)],color=color.cyan,
            radius=radBig,frame=NoPist))
    LSmoke = curve(pos=[(0,0,-0.1), (0,0,-0.1)],color=color.cyan, radius=radBig,
            frame=LRC) #these 3 lines are the LRC smoke
    CSmoke1 = curve(color=color.cyan, radius=radBig, frame=LRC)
    CSmoke2 = curve(color=color.cyan, radius=radBig, frame=LRC)
    lrcArrow = arrow(pos=(127.5,7.35), axis=(0,-2,0), length = 4, shaftwidth=1, 
        headlength = 1.5, color=color.red, frame=LRC)

    pbotgraph, ptopgraph, ptop, ptopxaxis = addPGraphs(Feedback) # pressure graphs
    tankPGraph = curve(pos = [(125,0), (130,0), (145.5,0)], 
        radius = radBig, color = color.cyan, frame = LRC)

    # mean-temperature graph
    TGraph=Frame()
    curve(pos=[(75,-30.25),(75,-7.25)],frame=TGraph, radius=radBig)
    curve(pos=[(75,-12.5),(83.5,-12.5)],frame=TGraph, radius=radBig) # x Axis
    Label(pos=(79,-5),frame=TGraph,text="Temperature (Centigrade)")
    Label(pos=(72.8,-12.4),frame=TGraph,text='30')
    Label(pos=(71.4,-26.1),frame=TGraph,text="-100")
    stirlingT = curve(pos=[(83.5, -12.5), (96, -26.25), (105, -26.25)],visible=0,  radius=radBig)
    isoT = curve(pos=[(145.5, -12.5), (125, -12.5), (96.6, -26.25),(95.7, -26.25),
        (83.5, -12.5)],visible=0, radius=radBig)

    SOvals, ovalCold, fillCold, vertLineCold, ovalHot, fillHot, vertLineHot, \
        IOval, ovalBuf, fillBuf, vertLineBuf, \
        TOvals, ovalNet, fillNet, vertLineNet, ovalBR, fillBR, vertLineBR, \
        ovalBL, fillBL, vertLineBL = addOvals() # add the p-v ellipses
    vertLineNet.y[0] = -5.5;  fillNet.color = pink # overwrite a tashe default
    CompOval = Frame() # add the one in the compliance
    ovalComp = curve(pos=nullPos,frame=CompOval, radius=radBig)
    vertLineComp = curve(pos=[(120,9.5,0.02),(120,25,0.02)],color=faint,frame=CompOval, radius=radBig)
    CompOval.show(False)

    regZoomed, regZooming, regBubble, topRegArrow, botRegArrow, pvsphere, txsphere, \
        ovalRegP, fillRegP, ovalRegT = addRegCloseup(km,'PTR') # regenerator closeup
    bufZoomed, bufZooming, bufBubble, bufpvsphere, buftxsphere, \
        ovalBufP, ovalBufT = addBufCloseup(km,'PTR') # buffer closeup

    # cold hx closeup:
    chxZoomed = Frame()
    chxZooming = Frame()
    chxArrows = Frame()
    chxBubble = box(y=5.25, height=0.25, width=0, color=color.cyan, frame=chxZooming)
    topChxArrow = arrow(length=0.25,  
        headlength=0.15, fixedwidth=1, color=color.red, frame=chxArrows)
    botChxArrow = arrow(length=0.25, 
        headlength=0.15, fixedwidth=1, color=color.red, frame=chxArrows)
    curve(pos=[(94.05,3.7), (94.05,2.5), (98.2,2.5)], radius=radBig/5, frame=chxZoomed) # T axes
    curve(pos=[(94.05,2.4), (94.05,1.2), (98.2,1.2)], radius=radBig/5, frame=chxZoomed) # p axes
    if km.lower() == 'm': 
        lab4 = Label(pos=(96.2,0.5), frame=chxZoomed,
                     text='Menu: stirling, optr, Optr, fptr, regenerator, p-tube, quit, Faster, Slower')
        if oldKey == 's':
            lab4.text = "Menu: stirling, optr, Optr, fptr, regenerator, quit, Faster, Slower"
        
    Label(pos=(94.7,3.5), frame=chxZoomed,text="Temperature")
    Label(pos=(96.7,1.05), frame=chxZoomed,text="Parcel location")
    Label(pos=(94.5,2.2), frame=chxZoomed,text="Pressure")
    chxpvsphere = sphere(radius=radBig/3.5, color=color.cyan, frame=chxZoomed)
    ovalChxP = curve(pos=nullPos, frame=chxZoomed, radius=radBig/10, color=color.cyan)
    chxtxsphere = sphere(radius=radBig/3.5, color=color.cyan, frame=chxZoomed)
    ovalChxT = curve(pos=nullPos, frame=chxZoomed, radius=radBig/10, color=color.cyan)
       
    if option == 'c': # the yellow "control volume"
        curve(pos=[(93,1.5),(93,16.5),(101,16.5),(101,1.5),(93,1.5)], radius=radBig, color=color.yellow)
        fatPiston = 1.
        rightPiston.length = 4
    else:
        fatPiston = 0
        
    # Animate
    while 1:
        rate(refreshRate) # Pause here, limiting frame update rate to "refreshRate." 
        wt += dwt
        sinwt = 2*sin(wt) # weird, but this was in PTR.bas!
        coswt = cos(wt)/2
        # clean up the math later; for now, just mimic ptr.bas
    #    leftPiston.x = 76 + rexL*coswt + imxL*sinwt
        leftPiston.x = 79 + 9.25*sin(.026737*110)*coswt + 100./119.*sinwt
    #    rightPiston.x = 100 + rexR*coswt + imxR*sinwt
        rightPiston.x = 101 + 5*sin(0.026737*(130))*coswt + 0.5455*sinwt
        bufPistonx = 121 + rexb*coswt - imxb*sinwt # temporary name, leftover?
        xinert = 100 + rexinert*coswt + imxinert*sinwt
        xd = 145 - (22.2*coswt + 0.7*sinwt)*0.85 
        xcv = 131.8 - leftPiston.x      # virtual xc, for purposes of interpolating in U bend
        x75b = (xcv + xinert - 15) / 2
        x80b = (x75b + xinert - 15) / 2
        x70b = (xcv + x75b) / 2

        for i in [0,1]: 
            smoke[0].x[i] = leftPiston.x + 1 
            smoke[1].x[i] = 85 + 8.0*sin(.026737*115)*coswt + 105./138.*sinwt # 1-3 are regen
            smoke[2].x[i] = 90 + 6.5*sin(.026737*120)*coswt + 110./169.*sinwt
            smoke[3].x[i] = 95 + 5.0*sin(.026737*125)*coswt + 115./220.*sinwt
            smoke[4].x[i] = rightPiston.x -1
            for n in [105,110,115,120]:  # which is 5,6,7,8; routine in tbt
                smoke[n/5-16].x[i] = n + 5*sin(0.026737*(n+30))*coswt + 0.5455*sinwt

    # LRC smoke.  n=125 passes through the inertance;  n=130 is in the compliance
            radCSmoke2 = 4-2*coswt+sinwt/2
            if ks.lower() == 'o' or ks == 'p':     
                xline = 125 + 5*sin(0.026737*155)*coswt + 0.5455*sinwt
                if xline < 125.:
                    LSmoke.x[i] = xline
                    LSmoke.y[i] = 4 + 10*i 
                elif xline < 126.25:
                    LSmoke.x[i] = 4*xline - 375
                    LSmoke.y[i] = 7.5 + 3*i 
                else:
                    CSmoke1.pos = arc(130, 9, 1+sqrt(xline-126.25), -90, 90)
                LSmoke.visible = xline<126.25
                CSmoke1.visible = not LSmoke.visible
                CSmoke2.pos = arc(130, 9, radCSmoke2, -90, 90)
                
    # For Optr view, we need more smoke, left of location zero
            if ks == 'O':
                for j in range(5):
                    n=55+5*j
                    leftSmoke[j].x[i] = n + 9.25*sin(0.026737*(n+30))*coswt + (n+20)/119.*sinwt
                    
            smoke[9].x[i] = xd   # net power input
            smoke[10].x[i] = xinert + 15 - 0.55*sinwt # bottom right, n = 115, was 0.4 sinwt
            if xinert > 101.5:
                smoke[11].x[i] = xinert + 3.5 # [11] is the feedback inertance, n = 100, DONE
            elif xinert < 98.5:
                smoke[11].x[i] = xinert - 3.5
            else:
                smoke[11].x[i] = 3.333333*xinert - 233.3333
        if xinert > 101.5 or xinert < 98.5: 
            smoke[11].y[0] = -4
            smoke[11].y[1] = -14
        else:
            smoke[11].y[0] = -7
            smoke[11].y[1] = -11

        xl = xinert - 15  #[12] is bottom left feedback, usually straight, n=85 in old notation
        if xl > 77.0:
            smoke[12].x[0] = xl;  smoke[12].y[0] = -4
            smoke[12].x[1] = xl;  smoke[12].y[1] = -14
        else:
            theta = (77 - xl) / 7.13
            smoke[12].x[0] = 77-3.171*sin(theta);  smoke[12].y[0] = -4*cos(theta)
            smoke[12].x[1] = 77-11.1*sin(theta);  smoke[12].y[1] = -14*cos(theta)
            
        xl = 76.7 - 14.54*coswt - 0.845*sinwt # 13 is farther left/up the curve; n=77bottom in old notation
        if xl > 77:
            smoke[13].x[0] = xl;  smoke[13].y[0] = -4
            smoke[13].x[1] = xl;  smoke[13].y[1] = -14
        else:
            theta = (77 - xl) / 7.13
            smoke[13].x[0] = 77-4*sin(theta);  smoke[13].y[0] = -4*cos(theta)
            smoke[13].x[1] = 77-14*sin(theta);  smoke[13].y[1] = -14*cos(theta)

        xl = 68.4 - 10.31*coswt - 0.845*sinwt # 14 is about midway around the left bend.  n=68b in old notation
        theta = (77 - xl) / 7.13 
        smoke[14].x[0] = 77 - 14*sin(theta)
        smoke[14].y[0] = -14*cos(theta)
        smoke[14].x[1] = 77 - 4*sin(theta)
        smoke[14].y[1] = -4*cos(theta)  

        xl = 71.7 + 6.07*coswt + 0.845*sinwt # 15 is uppermost around the left bend.  n=72t in old notation
        theta = (77 - xl) / 7.13 
        smoke[15].x[0] = 77 - 14*sin(theta)
        smoke[15].y[0] = 14*cos(theta)
        smoke[15].x[1] = 77 - 4*sin(theta)
        smoke[15].y[1] = 4*cos(theta)  
            
        pcold = 25 + repc*coswt - impc*sinwt
        p = 25 + reph*coswt + imph*sinwt
        ptank = 25 + 0.375*sinwt - 1.5*coswt

        rateL = 1.68*coswt - 0.23*sinwt
        rateR = 1.3933*coswt + 0.16667*sinwt
        ambientArrow.shaftwidth = rateL
        ambientArrow.visible = rateL>0
        remoteArrow.shaftwidth = -rateR
        remoteArrow.visible = rateR<0 and (ks != 'c' or zooming)
        
        if ks == 's':
            ptopgraph.x[0] = leftPiston.x + 1
            ptopgraph.x[3] = rightPiston.x - 1 - fatPiston
            ptopgraph.y[0] = ptopgraph.y[1] = p
            ptopgraph.y[2] = ptopgraph.y[3] = pcold
            if dtogl:
                if coswt > .707/2: words.text = "displace right"
                elif sinwt > .707*2: words.text = "expand"
                elif coswt < -.707/2: words.text = "displace left"
                else: words.text =  "compress"
        elif ks.lower() == 'o':
            if ks == 'O':
                ptopgraph.x[0] = 69
            else:
                ptopgraph.x[0] = leftPiston.x+1            
            ptopgraph.y[0] = ptopgraph.y[1] = p
            ptopgraph.y[2] = ptopgraph.y[3] = pcold
            tankPGraph.y[0] = pcold
            tankPGraph.y[1] = tankPGraph.y[2] = ptank
            lrcRate = 0.1467*sinwt + 0.004*coswt
            if lrcRate > 0:
                lrcArrow.shaftwidth = 1.7*lrcRate
            lrcArrow.visible = lrcRate>0    
        elif ks == 'f':
            ptopgraph.y[0] = ptopgraph.y[1] = p
            ptopgraph.y[2] = ptopgraph.y[3] = pcold
            pbotgraph.y[0] = pbotgraph.y[1] = p-51.5
            pbotgraph.y[2] = pbotgraph.y[3] = pcold-51.5
        elif ks == 'r':
            regBubble.x = (smoke[1].x[0]+smoke[2].x[0])/2.
            regBubble.length = (smoke[2].x[0]-smoke[1].x[0])/6
            dpdt = -repc * sinwt - impc * coswt
            dxdt = -rexr * sinwt - imxr * coswt
            shaftWidth = 0.05 * (dpdt / 3 - 3 * dxdt)
            if shaftWidth < 0:
                topRegArrow.y = 5.525
                topRegArrow.axis = (0,-1,0)
                botRegArrow.y = 4.975
                botRegArrow.axis = (0, 1,0)
            else:
                topRegArrow.y = 5.275
                topRegArrow.axis = (0, 1,0)
                botRegArrow.y = 5.225
                botRegArrow.axis = (0,-1,0)
            topRegArrow.x = botRegArrow.x = regBubble.x
            topRegArrow.shaftwidth = botRegArrow.shaftwidth = abs(shaftWidth)
            topRegArrow.length = botRegArrow.length = 0.25
            pvx = 5*regBubble.length + 87.5
            pvy = ((p+pcold)/2-29)/15 + 2.2 + 0.25 # final 0.25 added when fixing for DLG computer
            pvsphere.x = pvx;  pvsphere.y = pvy
            tx = regBubble.x
            ty = 2./3. + 1.25 - (tx-87.5)/3 + 0.25 # final 0.25 added when fixing for DLG computer
            txsphere.x = tx;  txsphere.y = ty
            if myCounter == 31 and wt - whenRegOvalsBegan < 6.9 and not zooming:
                ovalRegP.append(pos=(pvx, pvy, 0.01))
                ovalRegT.append(pos=(tx, ty, 0.01))
            elif fillRegP.pos.any() != ovalRegP.pos.any():
                fillRegP.pos = ovalRegP.pos

            #  I am not really sure I got the physics accurate, since "aspect" in
                # quickbasic has no close analog here.

        elif ks == 'p':
            bufBubble.x = (smoke[7].x[0]+smoke[6].x[0])/2.
            bufBubble.length = (smoke[7].x[0]-smoke[6].x[0])/6
            tx = bufBubble.x
            ty = pcold/7. - 2.5 
            buftxsphere.x = tx;  buftxsphere.y = ty
            pvx = 124 - pcold/7.
            pvy = ty
            bufpvsphere.x = pvx;  bufpvsphere.y = pvy
            if myCounter == 31 and wt - whenBufOvalsBegan < 6.9 and not zooming:
                ovalBufP.append(pos=(pvx, pvy, 0.01))
                ovalBufT.append(pos=(tx, ty, 0.01))
        elif ks == 'c': # cold heat exchanger close-up:
            chxBubble.x = (smoke[4].x[0]+3*smoke[3].x[0])/4
            chxBubble.length = (smoke[4].x[0]-smoke[3].x[0])/10
            topChxArrow.x = botChxArrow.x = chxBubble.x

            if km.lower() == 'm': 
                if oldKey == 's':
                    lab4.text = "Menu: stirling, optr, Optr, fptr, regenerator, quit, Faster, Slower"
                elif oldKey in ['o', 'O', 'f']:
                    lab4.text='Menu: stirling, optr, Optr, fptr, regenerator, p-tube, quit, Faster, Slower'
                    
            # Figure out the chx heat arrows, depending on where's the bubble:
            if chxBubble.x < 95.63: # it's in the regen
                chxArrows.show(ks == 'c' and not zooming)
                shaftWidth =  coswt/6.67 - sinwt/100
                if shaftWidth < 0:
                    topChxArrow.y = 5.525
                    topChxArrow.axis = (0,-1,0)
                    botChxArrow.y = 4.975
                    botChxArrow.axis = (0, 1,0)
                else:
                    topChxArrow.y = 5.275
                    topChxArrow.axis = (0, 1,0)
                    botChxArrow.y = 5.225
                    botChxArrow.axis = (0,-1,0)
                topChxArrow.shaftwidth = botChxArrow.shaftwidth = abs(shaftWidth)
            elif chxBubble.x > 95.77 and chxBubble.x < 96.73 and coswt < 0: # it's in the chx:
                topChxArrow.shaftwidth = botChxArrow.shaftwidth = 0.07
                topChxArrow.y = 5.525
                topChxArrow.axis = (0,-1,0)
                botChxArrow.y = 4.975
                botChxArrow.axis = (0, 1,0)
                chxArrows.show(ks == 'c' and not zooming)
            else: # it's in the pulse tube, or inbetween.     
                chxArrows.show(False)
            topChxArrow.length = botChxArrow.length = 0.25  # needed to overwrite a default.
            
            # now the chx pressure and temperature traces:
            chxpvsphere.x = chxBubble.x;  chxpvsphere.y = 1.7 + 0.5*coswt
            if chxBubble.x > 96.73:
                temper = 0.6*coswt - 0.184
            elif chxBubble.x > 95.7 and coswt < 0:
                temper = (95.7 - chxBubble.x) / 2.122
            elif chxBubble.x < 95.7:
                temper = (95.7 - chxBubble.x) / 5
            else:
                temper = 0.
            chxtxsphere.x = chxBubble.x;  chxtxsphere.y = temper + 3.2
            if myCounter == 31 and wt - whenChxOvalsBegan < 6.9 and not zooming:
                ovalChxP.append(pos=(chxpvsphere.x, chxpvsphere.y, 0.01))
                ovalChxT.append(pos=(chxtxsphere.x, chxtxsphere.y, 0.01))
            
        if zooming and myCounter < 30:  # zoom the scene:
            myCounter += 1  
            scene.center = scene.center + (dxcen, dycen)
            scene.range = scene.range.x + drange
            # kluge to move chx closer to regen for chx closeup view:
            if ks == 'c':
                incr = 0.45/30
                for i in rightHX + reg:  i.length += incr
            elif oldKey == 'c':
                for i in rightHX + reg:  i.length -= incr
            chxArrows.show(False)  # another kluge
        elif zooming and myCounter == 30:
            zooming = False
            myCounter += 1 # so we only do this once
            whenRegOvalsBegan = whenBufOvalsBegan = whenChxOvalsBegan = wt
        regZooming.show(ks == 'r')
        regZoomed.show(ks == 'r' and not zooming)
        bufZooming.show(ks == 'p')
        bufZoomed.show(ks == 'p' and not zooming)
        chxZooming.show(ks == 'c')
        chxZoomed.show(ks == 'c' and not zooming)

        if vtogl:
            for i in [0,1]:
                vertLineCold.x[i] = leftPiston.x+1
                vertLineHot.x[i] = rightPiston.x-1 - fatPiston
                vertLineBuf.x[i] = smoke[8].x[0]
                vertLineComp.x[i] = 130 + radCSmoke2
                vertLineNet.x[i] = xd
                vertLineBR.x[i] = smoke[10].x[0]
                vertLineBL.x[i] = (smoke[12].x[0]+smoke[12].x[1])/2
            vertLineCold.y[1] = p
            vertLineHot.y[1] = vertLineBuf.y[1] = pcold
            vertLineComp.y[1] = ptank
            vertLineBL.y[1] = p - 51.5
            vertLineBR.y[1] = vertLineNet.y[1] = pcold - 51.5

            if wt - whenOvalsBegan < 6.9:
                ovalHot.append(pos=(leftPiston.x + 1, p, 0.01))
                ovalCold.append(pos=(vertLineHot.x[i], pcold, 0.01))
                ovalBuf.append(pos=(smoke[8].x[0], pcold, 0.01))
                ovalComp.append(pos=(130 + radCSmoke2, ptank, 0.01))
                ovalNet.append(pos=(xd, pcold-51.5, 0.01))
                ovalBR.append(pos=(vertLineBR.x[0], pcold-51.5, 0.01))
                ovalBL.append(pos=(vertLineBL.x[0], p-51.5, 0.01))
            elif fillCold.pos.any() != ovalCold.pos.any():
                fillCold.pos = ovalCold.pos
                fillHot.pos = ovalHot.pos
                fillBuf.pos = ovalBuf.pos
                fillNet.pos = ovalNet.pos
                fillBR.pos = ovalBR.pos
                fillBL.pos = ovalBL.pos
                ovalCold.append(pos=(vertLineHot.x[i], pcold, 0.01)) # to increment the counter so this doesn't trip again and again
        
        if scene.kb.keys and option != 'none':
            wiseExit( __name__ , scene)
            return
                        
        if not zooming and (scene.kb.keys or firstTime): # keyboard event in scene?
            if not firstTime:  
                if key == 's' or key.lower() == 'o' or key == 'f' or key == 'r' or key == 'c' or key == 'p':
                    oldKey = key
                    xcenOld = scene.center.x
                    ycenOld = scene.center.y
                    rangeOld = scene.range.x
                key = scene.kb.getkey()
    #       Take care of zooming issues first:
            if (key == 's' or key.lower() == 'o' or key == 'f') and (oldKey == 'r' 
                or oldKey == 'p' or oldKey == 'c'):
                zooming = True
                dxcen = (xcenNorm - xcenOld) / 30.
                dycen = (ycenNorm - ycenOld) / 30.
                drange = (rangeNorm - rangeOld) / 30.
                myCounter = 0
            elif key == 'r' and oldKey != 'r':
                ks = 'r'
                zooming = True
                ovalRegP.pos=nullPos;  fillRegP.pos=nullPos;  ovalRegT.pos=nullPos
                dxcen = (xcenReg - xcenOld) / 30.
                dycen = (ycenReg - ycenOld) / 30.
                drange = (rangeReg - rangeOld) / 30.
                myCounter = 0
            elif key == 'c' and oldKey != 'c':
                ks = 'c'
                zooming = True
                ovalChxP.pos=nullPos;  ovalChxT.pos=nullPos  
                dxcen = (xcenCold - xcenOld) / 30.
                dycen = (ycenCold - ycenOld) / 30.
                drange = (rangeCold - rangeOld) / 30.
                myCounter = 0
            elif key == 'p' and ks != 's' and ks != 'r':
                ks = 'p'
                zooming = True
                ovalBufP.pos=nullPos;  ovalBufT.pos=nullPos
                dxcen = (xcenBuf - xcenOld) / 30.
                dycen = (ycenBuf - ycenOld) / 30.
                drange = (rangeBuf - rangeOld) / 30.
                myCounter = 0

    # Now decide what should be visible in the three overviews.
    #  show() works for Bill's Frames, and visible works for raw vpython objects.
            if key == 's':
                ks = 's'
                ptopxaxis.x[1]=105
                LeftPist.show(True)
                NoPist.show(False)
                Tbt.show(False)
                LRC.show(False)
                rightPiston.visible=1
                TGraph.show(True)
                stirlingT.visible = 1
                isoT.visible = 0
                Feedback.show(False)
                smoke[0].visible = 0
                for i in range(4,16):  smoke[i].visible = 0
                ptop.visible=1
                IOval.show(False)
                TOvals.show(False)
                if km.lower() == 'm': lab3.text = "stirling, optr, Optr, fptr, regen, coldX, v-togl, d-togl, quit, Faster, Slower"
            elif key.lower() == 'o':
                ks = key
                ptopxaxis.x[1] = 145.5
                ptopgraph.x[3] = 125
                Tbt.show(True)
                LRC.show(True)
                rightPiston.visible = 0
                Feedback.show(False)
                TGraph.show(True)
                stirlingT.visible = 0
                isoT.visible = 1
                words.text = ''
                ptop.visible=1
                IOval.show(vtogl)
                TOvals.show(False)
                if km.lower() == 'm': lab3.text = "stirling, optr, Optr, fptr, regen, coldX, p-tube, v-togl, quit, Faster, Slower"
                if key == 'o':
                    NoPist.show(False)
                    LeftPist.show(True) 
                    smoke[0].visible = 0
                else: # key=='O'
                    NoPist.show(True)
                    LeftPist.show(False)
                    smoke[0].visible = 1
            elif key == 'f':
                ks = 'f'
                ptopxaxis.x[1]=168
                ptopgraph.x[0]=69
                ptopgraph.x[3]=168
                LeftPist.show(False)
                NoPist.show(False)
                Tbt.show(True)
                LRC.show(False)
                smoke[0].visible = 1
                rightPiston.visible  = 0
                Feedback.show(True)
                TGraph.show(False)
                stirlingT.visible = 0
                isoT.visible = 0            
                words.text = ''
                ptop.visible=1
                IOval.show(vtogl)
                TOvals.show(vtogl)    
                if km.lower() == 'm': lab3.text = "stirling, optr, Optr, fptr, regen, coldX, p-tube, v-togl, quit, Faster, Slower"
            elif key == 'd':
                dtogl = not dtogl
                if not dtogl: words.text=''
            elif key == 'v':
                vtogl = not vtogl
                if vtogl: whenOvalsBegan = wt
            elif key == 'F':  dwt *= 2
            elif key == 'S':  dwt /= 2
            elif key.lower() == 'q':
                wiseExit( __name__ , scene)
                return
            else: pass
            if vtogl: #vtogl has just been changed to True:
                SOvals.show(True)
                IOval.show(ks.lower() == 'o' or ks == 'f')
                CompOval.show(ks.lower() == 'o')
                TOvals.show(ks == 'f')
            else: # vtogl has just been changed to False: 
                SOvals.show(False)
                IOval.show(False)
                CompOval.show(False)
                TOvals.show(False)
                ovalCold.pos=nullPos
                fillCold.pos=nullPos
                ovalHot.pos=nullPos
                fillHot.pos=nullPos
                ovalBuf.pos=nullPos
                fillBuf.pos=nullPos
                ovalComp.pos=nullPos
                ovalNet.pos=nullPos
                fillNet.pos=nullPos
                ovalBR.pos=nullPos
                fillBR.pos=nullPos
                ovalBL.pos=nullPos
                fillBL.pos=nullPos

            if firstTime:   # also use firstTime when a zoom out is complete.
                firstTime=False
                if key == 'r':
                    ks = 'r'
                    scene.center = (xcenReg, ycenReg)
                    scene.range = rangeReg
                    regZooming.show(True)
                    regZoomed.show(True)
                else:    
                    scene.center = (xcenNorm, ycenNorm)
#    end of definition of myWrap function

if __name__ == "__main__":
    myWrap('dummy')     

