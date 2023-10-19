""" Animation of Stirling engine and thermoacoustic-Stirling hybrid engine,
as described in Greg's thermoacoustics book.
Usage when typing in cmd:  'tashe.py' or 'tashe.py /opt' where opt can be [a,r,s,t,u].
This can also be called from a master.py, by typing 'master.py tashe' or 'master.py tashe-opt'
"""
from animTools import *   # which imports everything from visual
from feedbackers import * # functions shared by tashe and ptr

def myWrap(option):
    from inits import refreshRate, period, wt, coswt, sinwt, dwt, \
        firstTime, vtogl, dtogl, zooming, \
        purple, pink, darkgreen, lightgreen, lightblue, faint, rad, radBig
    longtitle='Thermoacoustic-Stirling Hybrid Engine Animation'
    whowhen='Quickbasic by GWS, 6/1994. Rev python by WCW & GWS, 2010-2015.'
    xcenNorm = 110.
    ycenNorm = -2.0
    rangeNorm = 53.
    xcenReg = 88.5
    ycenReg = 4.0
    rangeReg = 5.
    xcenBuf = 115.5
    ycenBuf = 4.0
    rangeBuf = 10.

    banner(longtitle,whowhen) # Show disclaimer in output window;  then
    #                           start graphical display:
    scene=Display(title=longtitle, center=(xcenNorm,200),
                  range=rangeNorm, userzoom=False, userspin=False)
    #Center.y will be redefined at firstTime test.

    if __name__ == '__main__':  option = caller()[1]
    #  Book options were a, r, s, t, u
    if option == 'a' or option == 's':
        key = 's'
        dtogl = 1
        vtogl = 1;
    elif option == 'r':
        key = 'r';  myCounter = 31
    elif option == 't':
        key = 't'
    elif option == 'u':
        key = 't'
        vtogl = 1
    else: option = 'none' #this takes care of typos, i.e. invalid options

    # More initial values
    reph = 7.0;  imph = 0.0
    repc = 9.0;  impc = -0.35

    rexh = -0.8;  imxh = -1.4
    rexc = 1.0;   imxc = -0.5
    rexb = -2.5;  imxb = -1.4
    rexinert = (rexc*impc - imxc*repc) * (reph - repc) / (reph*impc - imph*repc)
    imxinert = (rexc*impc - imxc*repc) * (imph - impc) / (reph*impc - imph*repc)
    rexr = (7.5 * rexh + 12.5 * rexc) / 20
    imxr = (7.5 * imxh + 12.5 * imxc) / 20
    lab3 = Label(pos=(110,-39), text="")
    whenOvalsBegan = whenBufOvalsBegan = whenRegOvalsBegan = wt

    if option == 'none':
        lab1 = Label(pos=(106,200-33),
            text='Type "m" to always show the menu, or any other key to always suppress it.')
        km = scene.kb.getkey()
        lab1.text = "    Type s, i, or t to start animation with"
        lab1.x = 80
        lab2 = Label(pos=(110,200-37),
            text=" Stirling, isolated Stirling, or thermoacoustic Stirling.")
        key = scene.kb.getkey() #get key to control initial view
        if key.lower() != 'i' and key.lower() != 't':  key = 's'
        lab1.visible = lab2.visible = 0
        
        if km.lower() == 'm': 
            lab3.text="stirling, isolated, thermoacoust, regen, buftube, v-togl, quit, Faster, Slower"
            if key == 's': lab3.text = "stirling, isolated, thermoacoust, regen, v-togl, d-togl, quit, Faster, Slower"
    else:
        km = 'none'
        lab3.visible = 0
    ks = '0';  oldKey = key

    reg, rightHX, ambientArrow, remoteArrow = addHeart() # The Stirling "heart" 
    for b in rightHX:  b.color = color.red
    # Make other objects visible momentarily, so Frame can make complete lists.
    LeftPist, leftPiston, rightPiston = addPistons() # the pistons
    curve(pos=[(75,14), (77,14)], frame=LeftPist, radius=radBig) # pipe around left piston
    curve(pos=[(75, 4), (77, 4)], frame=LeftPist, radius=radBig)
    rightPiston.color = color.red
    bufPiston=box(y=9,length=2,height=9.2,width=0, color=color.green, visible=0)  

    words = Label(pos=(117,9)) # Words describing piston motion
    ## font='helvetica.bold' or 'times new roman' seems to work in label, too.
    Tbt, Feedback = addPipes() # the tbt and feedback pipes, in two frames.
    Label(pos=(97,16),frame=Feedback,text="600 C")
    Label(pos=(77,0),frame=Feedback,text="30 C")
    Label(pos=(100,-4),frame=Feedback,text="30 C")
    Label(pos=(138,11.5),frame=Feedback,text="30 C")
    smoke = addSmoke() # smoke lines
    for i in [4,5,6,7]:  smoke[i].frame = Tbt
    for i in [0,8,9,10,11,12,13,14,15]:  smoke[i].frame = Feedback
    pbotgraph, ptopgraph, ptop, ptopxaxis = addPGraphs(Feedback) # pressure graphs

    # mean-temperature graph
    TGraph=Frame()
    curve(pos=[(75,-30.25),(75,-7.25)],frame=TGraph, radius=radBig) # Y Axis
    curve(pos=[(75,-26.25),(83.5,-26.25)],frame=TGraph, radius=radBig) 
    Label(pos=(79,-5),frame=TGraph,text="Temperature (Centigrade)")
    Label(pos=(72.2,-12.1),frame=TGraph,text='600')
    Label(pos=(73,-26.1),frame=TGraph,text="30")
    stirlingT = curve(pos=[(83.5, -26.25), (96, -12.5), (105, -12.5)],visible=0,  radius=radBig)
    isoT = curve(pos=[(145.5, -26.25), (120, -26.25), (96.6, -12.5),(95.7, -12.5),
        (83.5, -26.25)],visible=0, radius=radBig)

    SOvals, ovalCold, fillCold, vertLineCold, ovalHot, fillHot, vertLineHot, \
        IOval, ovalBuf, fillBuf, vertLineBuf, \
        TOvals, ovalNet, fillNet, vertLineNet, ovalBR, fillBR, vertLineBR, \
        ovalBL, fillBL, vertLineBL = addOvals() # add the p-v ellipses

    regZoomed, regZooming, regBubble, topRegArrow, botRegArrow, pvsphere, txsphere, \
        ovalRegP, fillRegP, ovalRegT = addRegCloseup(km,'tashe') # regenerator closeup
    bufZoomed, bufZooming, bufBubble, bufpvsphere, buftxsphere, \
        ovalBufP, ovalBufT = addBufCloseup(km,'tashe') # buffer closeup


    # Animate
    while 1:
        rate(refreshRate) # Pause here, limiting frame update rate to "refreshRate." 
        wt += dwt
        sinwt = sin(wt)
        coswt = cos(wt)
        leftPiston.x = 79 + rexc*coswt - imxc*sinwt
        rightPiston.x = 101 + rexh*coswt - imxh*sinwt
        bufPiston.x = 121 + rexb*coswt - imxb*sinwt
        xinert = 100 - rexinert*coswt + imxinert*sinwt
        xd = bufPiston.x + xinert - 74
        xcv = 131.8 - leftPiston.x      # virtual xc, for purposes of interpolating in U bend
        x75b = (xcv + xinert - 15) / 2
        x80b = (x75b + xinert - 15) / 2
        x70b = (xcv + x75b) / 2

        for i in [0,1]:  #making these smokes a linear interpolation between piston.x's.
            smoke[0].x[i] = leftPiston.x+1
            smoke[2].x[i] = (leftPiston.x+rightPiston.x)/2
            smoke[1].x[i] = (leftPiston.x+1+smoke[2].x[i])/2 
            smoke[3].x[i] = (smoke[2].x[i]+rightPiston.x-1)/2
            smoke[4].x[i] = rightPiston.x-1 
            smoke[6].x[i] = (smoke[4].x[i]+bufPiston.x-1)/2
            smoke[5].x[i] = (smoke[4].x[i]+smoke[6].x[i])/2 
            smoke[7].x[i] = (smoke[6].x[i]+bufPiston.x-1)/2
            smoke[8].x[i] = bufPiston.x-1
            smoke[9].x[i] = xd
            smoke[10].x[i] = xinert + 15  
            smoke[12].x[i] = xinert - 15  
            if xinert > 101.5:
                smoke[11].x[i] = xinert + 3.5
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
                
        if x80b > 77:  
            smoke[13].x[0] = x80b
            smoke[13].x[1] = x80b
            smoke[13].y[0] = -4
            smoke[13].y[1] = -14
        else:
            theta = (77 - x80b) / 7.13 
            smoke[13].x[0] = 77 - 14*sin(theta)
            smoke[13].y[0] = -14*cos(theta)
            smoke[13].x[1] = 77 - 4*sin(theta)
            smoke[13].y[1] = -4*cos(theta)  

        theta = (77 - x75b) / 7.13 
        smoke[14].x[0] = 77 - 14*sin(theta)
        smoke[14].y[0] = -14*cos(theta)
        smoke[14].x[1] = 77 - 4*sin(theta)
        smoke[14].y[1] = -4*cos(theta)  

        theta = (77 - x70b) / 7.13 
        smoke[15].x[0] = 77 - 14*sin(theta)
        smoke[15].y[0] = -14*cos(theta)
        smoke[15].x[1] = 77 - 4*sin(theta)
        smoke[15].y[1] = -4*cos(theta)  
            
        pcold = 25 + repc*coswt - impc*sinwt
        p = 25 + reph*coswt + imph*sinwt

        rateC = (-rexc*sinwt - imxc*coswt)
        rateH = (-rexh*sinwt - imxh*coswt)
        ambientArrow.shaftwidth = rateC
        ambientArrow.visible = rateC>0
        remoteArrow.shaftwidth = -rateH
        remoteArrow.visible = rateH<0

        if ks == 's':
            ptopgraph.x[0]=leftPiston.x+1
            ptopgraph.x[3]=rightPiston.x-1
            ptopgraph.y[0] = ptopgraph.y[1] = pcold
            ptopgraph.y[2] = ptopgraph.y[3] = p
            if dtogl:
                if coswt > .707: words.text = "displace right"
                elif sinwt > .707: words.text = "expand"
                elif coswt < -.707: words.text = "displace left"
                else: words.text =  "compress"
        elif ks == 'i':
            ptopgraph.x[0] = leftPiston.x+1
            ptopgraph.x[3] = bufPiston.x-1
            ptopgraph.y[0] = ptopgraph.y[1] = pcold
            ptopgraph.y[2] = ptopgraph.y[3] = p
        elif ks == 't':
            ptopgraph.y[0] = ptopgraph.y[1] = pcold
            ptopgraph.y[2] = ptopgraph.y[3] = p
            pbotgraph.y[0] = pbotgraph.y[1] = pcold-51.5
            pbotgraph.y[2] = pbotgraph.y[3] = p-51.5
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
            pvy = (pcold-29)/15 + 2.2 + 0.25 # final 0.25 added when fixing for DLG computer
            pvsphere.x = pvx;  pvsphere.y = pvy
            tx = regBubble.x
            ty = 7./3.+ (tx-87.5)/3 -0.25 + 0.25 # final 0.25 added when fixing for DLG computer
            txsphere.x = tx;  txsphere.y = ty
            if myCounter == 31 and wt - whenRegOvalsBegan < 6.9 and not zooming:
                ovalRegP.append(pos=(pvx, pvy, 0.01))
                ovalRegT.append(pos=(tx, ty, 0.01))
            elif fillRegP.pos.any() != ovalRegP.pos.any():
                fillRegP.pos = ovalRegP.pos

            #  I am not really sure I got the physics accurate, since "aspect" in
                # quickbasic has no close analog here.

        elif ks == 'b':
            bufBubble.x = (smoke[7].x[0]+smoke[6].x[0])/2.
            bufBubble.length = (smoke[7].x[0]-smoke[6].x[0])/6
            tx = bufBubble.x
            ty = p/7. - 2.5 
            buftxsphere.x = tx;  buftxsphere.y = ty
            pvx = 124 - p/7.
            pvy = ty
            bufpvsphere.x = pvx;  bufpvsphere.y = pvy
            if wt - whenBufOvalsBegan < 6.9 and not zooming:
                ovalBufP.append(pos=(pvx, pvy, 0.01))
                ovalBufT.append(pos=(tx, ty, 0.01))
            
        if zooming and myCounter < 30:
            myCounter += 1  
            scene.center = scene.center + (dxcen, dycen)
            scene.range = scene.range.x + drange
        elif zooming and myCounter == 30:
            zooming = False 
            whenRegOvalsBegan = wt;  whenBufOvalsBegan = wt
            myCounter += 1 # so we only do that once
        regZooming.show(ks == 'r')
        regZoomed.show(ks == 'r' and not zooming)
        bufZooming.show(ks == 'b')
        bufZoomed.show(ks == 'b' and not zooming)

        if vtogl:
            for i in [0,1]:
                vertLineCold.x[i] = leftPiston.x+1
                vertLineHot.x[i] = rightPiston.x-1
                vertLineBuf.x[i] = bufPiston.x-1
                vertLineNet.x[i] = xd
                vertLineBR.x[i] = xinert+15
                vertLineBL.x[i] = xinert-15
            vertLineCold.y[1] = pcold
            vertLineHot.y[1] = vertLineBuf.y[1] = vertLineNet.y[1] = p
            vertLineBR.y[1] = p - 51.5
            vertLineBL.y[1] = pcold - 51.5

            if wt - whenOvalsBegan < 6.9:
                ovalCold.append(pos=(leftPiston.x + 1, pcold, 0.01))
                ovalHot.append(pos=(rightPiston.x - 1, p, 0.01))
                ovalBuf.append(pos=(bufPiston.x - 1, p, 0.01))
                ovalNet.append(pos=(xd, p, 0.01))
                ovalBR.append(pos=(xinert+15, p-51.5, 0.01))
                ovalBL.append(pos=(xinert-15, pcold-51.5, 0.01))
            elif fillCold.pos.any() != ovalCold.pos.any(): # if time>2pi and not yet filled:
                fillCold.pos = ovalCold.pos
                fillHot.pos = ovalHot.pos
                fillBuf.pos = ovalBuf.pos
                fillNet.pos = ovalNet.pos
                fillBR.pos = ovalBR.pos
                fillBL.pos = ovalBL.pos
        
        if scene.kb.keys and option != 'none':
            wiseExit( __name__ , scene)
            return
           
        if not zooming and (scene.kb.keys or firstTime): # keyboard event in scene?
            if not firstTime:  
                if key == 's' or key == 'i' or key == 't' or key == 'r' or key == 'b':
                    oldKey = key
                    xcenOld = scene.center.x
                    ycenOld = scene.center.y
                    rangeOld = scene.range.x
                key = scene.kb.getkey()
    #       Take care of zooming issues first:
            if (key == 's' or key == 'i' or key == 't') and (oldKey == 'r' 
                or oldKey == 'b'):
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
            elif key == 'b' and ks != 's' and ks != 'r':
                ks = 'b'
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
                Tbt.show(False)
                rightPiston.visible=1
                bufPiston.visible=0
                TGraph.show(True)
                stirlingT.visible = 1
                isoT.visible = 0
                Feedback.show(False)
                for i in range(4,16):  smoke[i].visible = 0
                ptop.visible=1
                IOval.show(False)
                TOvals.show(False)
                if km.lower() == 'm': lab3.text = "stirling, isolated, thermoacoust, regen, v-togl, d-togl, quit, Faster, Slower"
            elif key == 'i':
                ks = 'i'
                ptopxaxis.x[1] = 125
                LeftPist.show(True)
                Tbt.show(True)
                rightPiston.visible = 0
                bufPiston.visible = 1
                Feedback.show(False)
                TGraph.show(True)
                stirlingT.visible = 0
                isoT.visible = 1
                words.text = ''
                ptop.visible=1
                IOval.show(vtogl)
                TOvals.show(False)
                if km.lower() == 'm': lab3.text = "stirling, isolated, thermoacoust, regen, buftube, v-togl, quit, Faster, Slower"
            elif key == 't':
                ks = 't'
                ptopxaxis.x[1]=168
                ptopgraph.x[0]=69
                ptopgraph.x[3]=168
                LeftPist.show(False)
                Tbt.show(True)
                rightPiston.visible = bufPiston.visible = 0
                Feedback.show(True)
                TGraph.show(False)
                stirlingT.visible = 0
                isoT.visible = 0            
                words.text = ''
                ptop.visible=1
                IOval.show(vtogl)
                TOvals.show(vtogl)
                if km.lower() == 'm': lab3.text = "stirling, isolated, thermoacoust, regen, buftube, v-togl, quit, Faster, Slower"
            elif key == 'd':
                dtogl = not dtogl
                if not dtogl: words.text=''
            elif key == 'v':
                vtogl = not vtogl
                if vtogl:  whenOvalsBegan = wt
            elif key.upper() == 'F':  dwt *= 2
            elif key == 'S':  dwt /= 2
            elif key.lower() == 'q':
                wiseExit( __name__ , scene)
                return
            else: pass
            if vtogl: #vtogl has just been changed to True:
                SOvals.show(True)
                IOval.show(ks == 'i' or ks == 't')
                TOvals.show(ks == 't')
            else: # vtogl has just been changed to False: 
                SOvals.show(False)
                IOval.show(False)
                TOvals.show(False)
                ovalCold.pos=nullPos
                fillCold.pos=nullPos
                ovalHot.pos=nullPos
                fillHot.pos=nullPos
                ovalBuf.pos=nullPos
                fillBuf.pos=nullPos
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
