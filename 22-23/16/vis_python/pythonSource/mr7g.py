""" mr7, a master py that selects among many animation-option's in thermoacoustics book.

    usage examples:
    mr7.py wave
    mr7.py wave-opt where opt in [k,s,t,u,v]
If no specific animiation is named, open a controls window with a mouse-selectable menu.
When bundling this in mac with py2app, copy this to "thermoac.py" so bundle is named thermoac.
"""

import sys, os

def dummy():
    return

def caller2():
    """ Adapted from caller() in AnimTools.
    Find out how the op sys started the animation.
    Account for something like path\path\master.py -animationName-option
         or master.py animationName
    Be careful of punctuation in the path.
    """
    progName = sys.argv[0].split('\\')[-1].split('/')[-1].lower()

    if len(sys.argv) == 2: # programName, blank, OptionString:
        progOptionString = sys.argv[1].lower().replace(' ','').replace('/','-').split('-')
        if progOptionString[0] == '': del progOptionString[0]
        aniName = progOptionString[0]
        if len(progOptionString) > 1:
            myOption = progOptionString[1]
        else:
            myOption = 'none'   
    else:  # only programName (e.g. master.py) is present
        aniName = 'none'
        myOption = 'none'
        # programName-option.  Or, no option
        #print 'Correct syntax:  "', progName, 'animation"  or  "', progName, '-animation"'
        #print '              or "', progName, 'animation-option"  or  "', progName, '-animation-option"'
        #print '              or "', progName, 'animation/option"  or  "', progName, '-animation/option"'
        #print '              or "', progName, '/animation"  or  "', progName, '/animation/option"'
        #os._exit(1)
    return aniName, myOption


aniName, aniOption = caller2()
if aniName == 'oscwall':
    import viscous
    viscous.myWrap('o')
elif aniName == 'ptr':
    import PTR
    PTR.myWrap(aniOption)
elif aniName == 'standing':
    import standing
    standing.myWrap(aniOption)
elif aniName == 'tashe':
    import Tashe
    Tashe.myWrap(aniOption)
elif aniName == 'thermal':
    import thermal
    thermal.myWrap(aniOption)
elif aniName == 'viscous':
    import viscous
    viscous.myWrap(aniOption)
elif aniName == 'wave':
    import wave
    wave.myWrap(aniOption)
else:
    from visual.controls import controls, button
    import  PTR, standing, Tashe, thermal, viscous, wave
    from vis import crayola;  color = crayola
    
    c = controls(x=0,y=0,width=420,height=700,range=60,title='thermoacoustic animations', background=(0.6,0.6,0.6))	
    c.display.fov = 0.001
    hint1 = button(pos=(13,56.5,0), height=14, width=54, color=(0.5,0.5,0.5),
                   text='Click a button to run an animation.', action=lambda: dummy())
    hint2 = button(pos=(17.5,53,0), height=12, width=43, color=(0.5,0.5,0.5),
                   text='Only one at a time, please.', action=lambda: dummy())

    buts = [ [ ], [ ], [ ] ]   # The buttons are in a list of lists.
    for j in range(3):         # Three columns of buttons.  The first index is the column number.
        for i in range(12-2*j):
            buts[j].append(button(pos=(25*(j-1),55-10*(i+j),0), height=10, width=25, 
			text='dummy', action=lambda: dummy()))
    buts[0][0].text='oscwall';       buts[0][0].action=lambda: viscous.myWrap('o')
    buts[0][0].button.color=(1,0.7,0.7)	#RGB model
    buts[0][1].text='PTR';           buts[0][1].action=lambda: PTR.myWrap('none')
    buts[0][2].text='PTR /c';        buts[0][2].action=lambda: PTR.myWrap('c')
    buts[0][3].text='PTR /p';        buts[0][3].action=lambda: PTR.myWrap('p')    
    buts[0][4].text='PTR /r';        buts[0][4].action=lambda: PTR.myWrap('r')    
    buts[0][5].text='PTR /s';        buts[0][5].action=lambda: PTR.myWrap('s')    
    for j in range(5):  buts[0][j+1].button.color=(0,1,.6)	#RGB model
    buts[0][6].text='standing';      buts[0][6].action=lambda: standing.myWrap('none')
    buts[0][7].text='standing /c';   buts[0][7].action=lambda: standing.myWrap('c')
    buts[0][8].text='standing /e';   buts[0][8].action=lambda: standing.myWrap('e')
    buts[0][9].text='standing /k';   buts[0][9].action=lambda: standing.myWrap('k')
    buts[0][10].text='standing /m';  buts[0][10].action=lambda: standing.myWrap('m')
    buts[0][11].text='standing /r';  buts[0][11].action=lambda: standing.myWrap('r')
    for j in range(6):  buts[0][j+6].button.color=color.orange
    buts[1][0].text='tashe';       buts[1][0].action=lambda: Tashe.myWrap('none')
    buts[1][1].text='tashe /a';    buts[1][1].action=lambda: Tashe.myWrap('a')
    buts[1][2].text='tashe /r';    buts[1][2].action=lambda: Tashe.myWrap('r') 
    buts[1][3].text='tashe /s';    buts[1][3].action=lambda: Tashe.myWrap('s')   
    buts[1][4].text='tashe /t';    buts[1][4].action=lambda: Tashe.myWrap('t')   
    buts[1][5].text='tashe /u';    buts[1][5].action=lambda: Tashe.myWrap('u')
    for j in range(6):  buts[1][j].button.color=color.green
    buts[1][6].text='thermal';     buts[1][6].action=lambda: thermal.myWrap('none')
    buts[1][7].text='thermal /e';  buts[1][7].action=lambda: thermal.myWrap('e')
    buts[1][8].text='thermal /w';  buts[1][8].action=lambda: thermal.myWrap('w')
    buts[1][9].text='thermal /y';  buts[1][9].action=lambda: thermal.myWrap('y')
    for j in range(4):  buts[1][j+6].button.color=color.yellow
    buts[2][0].text='viscous';      buts[2][0].action=lambda: viscous.myWrap('none')
    buts[2][1].text='viscous /m';   buts[2][1].action=lambda: viscous.myWrap('m') 
    buts[2][0].button.color=(1,0.7,0.7)	#RGB model
    buts[2][1].button.color=(1,0.7,0.7)	#RGB model
    buts[2][2].text='wave';         buts[2][2].action=lambda: wave.myWrap('none')
    buts[2][3].text='wave /k';      buts[2][3].action=lambda: wave.myWrap('k')
    buts[2][4].text='wave /s';      buts[2][4].action=lambda: wave.myWrap('s')
    buts[2][5].text='wave /t';      buts[2][5].action=lambda: wave.myWrap('t')
    buts[2][6].text='wave /u';      buts[2][6].action=lambda: wave.myWrap('u')
    buts[2][7].text='wave /v';      buts[2][7].action=lambda: wave.myWrap('v')
    for j in range(6):  buts[2][j+2].button.color=(0,.7,1)

    exitButton=button(pos=(25,-55,0), height=10, width=25, 
			text='EXIT', action=lambda: os._exit(1))
    
