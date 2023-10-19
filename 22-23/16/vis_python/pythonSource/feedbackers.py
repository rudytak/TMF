""" These functions are used by animations tashe and ptr.
"""
from numpy import empty
nullPos= empty([0,3])

def addSmoke():
    # smoke lines.
    #   x80 0  in tashe, this is ambient piston face
    #   x85 1  regen
    #   x90 2  regen
    #   x95 3  regen
    #  x100 4  in tashe (or both?) this is remote (hot or cryo) piston face
    #  x105 5
    #  x110 6   tbt
    #  x115 7
    #  x120 8  this is "isolated" ambient piston face
    #       9 net input/output
    #      10 tashe bottom right
    #      11 inertance
    #      12 tashe bottom left, in straight pipe
    #      13 tashe lowest of curvy ones
    #      14 tashe middle of curvy ones
    #      15 tashe highest of curvy ones
    from visual import curve, color
    from inits import radBig
    smoke = []
    for i in range(16): 
        smoke.append(curve(pos=[(0,4,-0.2),(0,14,-0.2)],color=color.cyan,radius=radBig))
    smoke[9].y[0] = -5;  smoke[9].y[1] = 5
    smoke[10].y[0] = -4;  smoke[10].y[1] = -14
    smoke[12].y[0] = -4;  smoke[12].y[1] = -14
    return smoke

def addHeart():
    # Draw the Stirling "heart" into scene;  always visible, so no Frame needed.
    from visual import box, curve, arrow, color, arange
    from inits import radBig
    yplates = arange(4.5, 14, .5)
    rightHX = [];  reg = []
    for y in yplates:
        box(pos=(82.25,y,0),length=0.5,height=0.2,width=0, color=color.green)
        reg.append(box(pos=(89.25,y,0),length=12.3,height=0.105,width=0))
        rightHX.append(box(pos=(96.25,y,0),length=0.5,height=0.2,width=0))
    curve(pos=[(77,14), (105,14)], radius=radBig) #resonoator top
    curve(pos=[(77,4), (105,4)], radius=radBig) # resonator bottom
    ambientArrow = arrow(pos=(82.25,3.8), axis=(0,-2,0), length = 4, shaftwidth=1, 
        headlength = 1.5, color=color.red)
    remoteArrow = arrow(pos=(96.25,-0.1), axis=(0,2,0), length = 4, shaftwidth=1, 
        headlength = 1.5, color=color.red)
    return reg, rightHX, ambientArrow, remoteArrow

def addPistons():
    from visual import box, curve, color
    from animTools import Frame
    from inits import radBig
    # Left piston, aka cold piston
    LeftPist=Frame()
    leftPiston=box(y=9,length=2,height=9.2,width=0, color=color.green, frame=LeftPist, radius=radBig) 
    # Right piston, aka hot or cryogenic piston
    rightPiston=box(y=9,length=2,height=9.2,width=0, visible=0)  
    return LeftPist, leftPiston, rightPiston

def addPipes():
    from visual import curve
    from animTools import Frame, arc
    from inits import radBig
    # tbt, aka buffer tube
    Tbt=Frame()
    curve(pos=[(105,4), (125,4)], frame=Tbt, radius=radBig)
    curve(pos=[(105,14), (125,14)], frame=Tbt, radius=radBig)
    # feedback pipes    
    Feedback = Frame()
    ib = curve(frame=Feedback, radius=radBig)  # ib is inner, bottom
    for pt in arc(77,0,4,90,270): ib.append(pos=pt)
    for pt in [(95,-4), (95,-7), (105,-7), (105,-4), (125,-4)]: ib.append(pos=pt)
    arc2 = curve(frame=Feedback, radius=radBig)
    for pt in arc(125,0,4,-90,90): arc2.append(pos=pt)
    ob = curve(frame=Feedback, radius=radBig)  # outer, bottom
    for pt in arc(77,0,14,90,270): ob.append(pos=pt)
    for pt in [(95,-14), (95,-11),(105,-11),(105,-14),(125,-14)]: ob.append(pos=pt)
    for pt in arc(125,0,14,270,339.075): ob.append(pos=pt)
    ob.append(pos=(168,-5))
    tr = curve(pos=[(168,5)], frame=Feedback, radius=radBig) # top right
    for pt in arc(125,0,14,20.925,90): tr.append(pos=pt)
    return Tbt, Feedback

def addPGraphs(Feedback):
    from visual import curve, color
    from animTools import Frame, Label
    from inits import radBig
    # bottom pressure graph, for Feedback view
    pbotgraph = curve(pos=[(69,-26.5),(95,-26.5),(105,-26.5),(168,-26.5)], 
        color=color.cyan,frame=Feedback, radius=radBig)
    curve(pos=[(69,-26.5,-0.1),(168,-26.5,-0.1)],frame=Feedback, radius=radBig) # x axis
    curve(pos=[(69,-18.5),(69,-34.5)],frame=Feedback, radius=radBig)  # y axis
    Label(pos=(71,-16.5),frame=Feedback,text="Pressure (MPa)")
    Label(pos=(66.5,-19),frame=Feedback,text="3.3")
    Label(pos=(66.5,-26.5),frame=Feedback,text="3.0")
    Label(pos=(66.5,-34),frame=Feedback,text="2.7")
    # top pressure graph, which is three line segments
    ptop=Frame()
    ptopgraph = curve(pos=[(80,25,0.02),(81.5,25,0.02),(96.5,25,0.02),(100,25,0.02)], 
        color=color.cyan,frame=ptop, radius=radBig)
    ptopxaxis = curve(pos=[(69,25,-0.1),(105,25,-0.1)],frame=ptop, radius=radBig)
    ptopyaxis = curve(pos=[(69,17),(69,33)],frame=ptop, radius=radBig)
    Label(pos=(71,35),frame=ptop,text="Pressure (MPa)")
    Label(pos=(66.5,32.5),frame=ptop,text="3.3")
    Label(pos=(66.5,25),frame=ptop,text="3.0")
    Label(pos=(66.5,17.5),frame=ptop,text="2.7")
    return pbotgraph, ptopgraph, ptop, ptopxaxis

def addOvals():
    # pv ellipse philosophy:
    # Start to draw them all when scene is s, t, or i, when vtogl is tripped.
    # Only control visibility via s, t, or i. Thus, 3 Frames are needed.
    # Null them all when vtogl is turned off.
    # Therefore, calculate pbottom, xbuf, etc even if they are not displayed.
    # Zooming also affects these.
    from visual import curve, convex, color
    from animTools import Frame
    from inits import purple, pink, faint, radBig
    SOvals = Frame()
    ovalLeft = curve(pos=nullPos, frame=SOvals, radius=radBig)
    fillLeft = convex(pos=nullPos, color=purple, frame=SOvals)
    vertLineLeft = curve(pos=[(80,14.5,0.02),(80,25,0.02)], color=faint, frame=SOvals, radius=radBig)
    ovalRight = curve(pos=nullPos,frame=SOvals, radius=radBig)
    fillRight = convex(pos=nullPos, color=purple, frame=SOvals)
    vertLineRight = curve(pos=[(100,14.5,0.02),(100,25,0.02)],color=faint,frame=SOvals, radius=radBig)
    SOvals.show(False)
    IOval  = Frame()
    ovalBuf = curve(pos=nullPos,frame=IOval, radius=radBig)
    fillBuf = convex(pos=nullPos, color=purple, frame=IOval)
    vertLineBuf = curve(pos=[(120,14.5,0.02),(120,25,0.02)],color=faint,frame=IOval, radius=radBig)
    IOval.show(False)
    TOvals = Frame()
    ovalNet = curve(pos=nullPos, frame=TOvals, radius=radBig)
    fillNet = convex(pos=nullPos, color=purple, frame=TOvals)
    vertLineNet = curve(pos=[(145,5.5,0.02),(145,25,0.02)],color=faint, frame=TOvals, radius=radBig)
    ovalBR = curve(pos=nullPos, frame=TOvals, radius=radBig)
    fillBR = convex(pos=nullPos, color=pink, frame=TOvals)
    vertLineBR = curve(pos=[(115,-14.5,0.02),(115,-20,0.02)],color=faint,frame=TOvals, radius=radBig)
    ovalBL = curve(pos=nullPos, frame=TOvals, radius=radBig)
    fillBL = convex(pos=nullPos, color=pink, frame=TOvals)
    vertLineBL = curve(pos=[(85,-14.5,0.02),(85,-20,0.02)],color=faint,frame=TOvals, radius=radBig)
    TOvals.show(False)
    return SOvals, ovalLeft, fillLeft, vertLineLeft, ovalRight, fillRight, vertLineRight, \
        IOval, ovalBuf, fillBuf, vertLineBuf, \
        TOvals, ovalNet, fillNet, vertLineNet, ovalBR, fillBR, vertLineBR, \
        ovalBL, fillBL, vertLineBL
        
def addRegCloseup(km,anim):
    # regenerator closeup
    from visual import curve, convex, color, sphere, arrow, box
    from animTools import Frame, Label
    from inits import radBig
    regZoomed = Frame()
    regZooming = Frame()
    regBubble = box(y=5.25, height=0.35, width=0, color=color.cyan, frame=regZooming)
    topRegArrow = arrow(length=0.25,  
        headlength=0.15, fixedwidth=1, color=color.red, frame=regZoomed)
    botRegArrow = arrow(length=0.25, 
        headlength=0.15, fixedwidth=1, color=color.red, frame=regZoomed)
    # try to move all this up 0.25, for smaller height in DLG pc
    curve(pos=[(90.5,3.25), (90.5,1.2), (93,1.2)], radius=radBig/5, frame=regZoomed) # p axes
    curve(pos=[(85,3.25), (85,1.2), (89.5,1.2)], radius=radBig/5, frame=regZoomed) # T axes   
    if anim == 'tashe':
        curve(pos=[(85,1.5),(89.5,3.0)], radius=radBig/5, frame=regZoomed) # T vs x
        if km.lower() == 'm':  Label(pos=(88.3,0.45), frame=regZoomed, # was y=0.25
            text="Menu: stirling, isolated, thermoacoustic, quit, Faster, Slower")
    else: # 'PTR'
        curve(pos=[(85,3.0),(89.5,1.5)], radius=radBig/5, frame=regZoomed) # T vs x
        if km.lower() == 'm':  Label(pos=(88.3,0.45), frame=regZoomed, #was y=0.25
            text="Menu: stirling, optr, Optr, fptr, coldX, quit, Faster, Slower")
    Label(pos=(86,3.25), frame=regZoomed,text="Temperature")
    Label(pos=(87.5,0.95), frame=regZoomed,text="Parcel location")
    Label(pos=(91.2,3.25), frame=regZoomed,text="Pressure")
    Label(pos=(92,0.95), frame=regZoomed,text="Parcel volume")
    pvsphere = sphere(radius=radBig/2, color=color.cyan, frame=regZoomed)
    txsphere = sphere(radius=radBig/2, color=color.cyan, frame=regZoomed)
    ovalRegP = curve(pos=nullPos, frame=regZoomed, radius=radBig/5, color=color.cyan)
    fillRegP = convex(pos=nullPos, frame=regZoomed, color=color.green)
    ovalRegT = curve(pos=nullPos, frame=regZoomed, radius=radBig/5, color=color.cyan)
    regZooming.show(False)
    regZoomed.show(False)
    return regZoomed, regZooming, regBubble, topRegArrow, botRegArrow, \
        pvsphere, txsphere, ovalRegP, fillRegP, ovalRegT

def addBufCloseup(km,anim):
    # tbt closeup
    from visual import curve, color, sphere, box
    from animTools import Frame, Label
    from inits import radBig
    bufZoomed = Frame()
    bufZooming = Frame()
    bufBubble = box(y=9.25, height=0.35, width=0, color=color.cyan, frame=bufZooming)
    curve(pos=[(117.5,3), (117.5,-1.05), (123,-1.05)], radius=radBig/5, frame=bufZoomed) # p axes
    curve(pos=[(108,3), (108,-1.05), (116.5,-1.05)], radius=radBig/5, frame=bufZoomed) # T axes
    if km.lower() == 'm':  
        if anim == 'tashe':
            Label(pos=(115,-3.1), frame=bufZoomed, # was y=-3.5
                text="Menu: stirling, isolated, thermoacoustic, regenerator, quit, Faster, Slower")
        else: # 'PTR':
            Label(pos=(115,-3.1), frame=bufZoomed,  # was y = -3.5
                text="Menu: stirling, optr, Optr, fptr, regen, coldX, quit, Faster, Slower")
    Label(pos=(109.9,2.9), frame=bufZoomed,text="Temperature")
    Label(pos=(112,-1.5), frame=bufZoomed,text="Parcel location")
    Label(pos=(118.8,2.9), frame=bufZoomed,text="Pressure")
    Label(pos=(120.5,-1.5), frame=bufZoomed,text="Parcel volume")
    bufpvsphere = sphere(radius=radBig, color=color.cyan, frame=bufZoomed)
    buftxsphere = sphere(radius=radBig, color=color.cyan, frame=bufZoomed)
    ovalBufP = curve(pos=nullPos, frame=bufZoomed, radius=radBig/5, color=color.cyan)
    ovalBufT = curve(pos=nullPos, frame=bufZoomed, radius=radBig/5, color=color.cyan)
    return bufZoomed, bufZooming, bufBubble, bufpvsphere, buftxsphere, \
        ovalBufP, ovalBufT
