from visual import *
""" A few functions and classes to extend VPython for thermoacoustic animations.
"""

nullPos = empty([0,3]) # because pos=[] does not work in vpython6

def wiseExit(name, scene):
    if name == "__main__":
        import os;  os._exit(1)
    else:
        scene.exit=False
        scene.visible = False 
        del scene
        
def banner(title='', author=''):
    print '##### ',title,' #####'
    print 
    print author
    print 'Los Alamos National Security, LLC.'
    print 'This Software was produced under a U.S. Government'
    print 'contract (DE-AC52-06NA25396) by Los Alamos National'
    print 'Laboratory, which is operated by Los Alamos National'
    print "Security, LLC, (LANS) for the U.S. Department of Energy's"
    print 'National Nuclear Security Administration. The U.S.'
    print 'Government is licensed to use, reproduce, and distribute'
    print 'this Software. Permission is granted to the public to copy'
    print 'and use this Software without charge, provided that this'
    print 'Notice and any statement of authorship are reproduced on'
    print 'all copies. Neither the Government nor LANS makes any'
    print 'warranty, express or implied, or assumes any liability or'
    print 'responsibility for the use of this Software.' 
    print

def show(obj, state=None):
    """Set the visible tag of an object, or, if an object.show() exists,
    (see VPyTools.Frame class), propagate the call to set internal
    objects.  Call with a Boolean argument, or None to toggle current
    visibility state."""
    if hasattr(obj,'show'):
        obj.show(state)
    else:
        if state == None:
            obj.visible = not obj.visible
        else:
            obj.visible = state

class Frame(frame):
    """Subclass visual's frame to add some convenient functions.  Specifically,
    make the .visible attribute do what you expect (show or hide all the
    objects in a frame).  Auto layout method also 'under development'.
    
     The new features page for vpython 5 says frame now has attribute visible,
     but it still doesn't work right when it contains a list of curves instead
     of just several individual curves.  So I'll continue using Bill's Frame.
    """
    def show(self, state=None):
        """ Set visibility of all objects in the frame to 'state'.  If state is absent,
        toggle the visibility.  Note that the .objects attribute does not report
        hidden objects, so first a parallel list has to be created.
        I THINK THE FIRST CALL HAS TO BE FROM A STATE OF FULL VISIBILITY.
        """
        if not hasattr(self,'all_objects'): #store all objects (not just visible)
            self.all_objects = self.objects[:]
        if state == None:
            self.visible = not self.visible
        else:
            self.visible = state
        for obj in self.all_objects:
            show(obj,self.visible)
    def animate(self, *args):
        """ Animate all the visible objects in the frame that have their own
        animate() functions defined.  Pass through everything in *args.
        """
        if self.visible:
            for o in self.objects:
                if o and hasattr(o,'animate'):
                    o.animate(*args)
    def layout(self, style='vertical', vspace = None, hspace = 1.0):
        if style == 'horizontal':
            x = 0.0
            for obj in self.objects:
                obj.x = x
                x += hspace
        else:
            y = 0.0
            if not vspace:
                obj = self.objects[0]
                # if obj is another frame, continue until there is a primitive:
                while hasattr(obj,'objects'):
                    obj = obj.objects[0]
                if hasattr(obj,'radius'):
                    vspace = 1*obj.radius
                elif hasattr(obj,'height'):
                    vspace = 2*obj.height
                elif hasattr(obj,'axis'):
                    vspace = mag(obj.axis) ## Use y component?
                else:
                    vspace = 1.0
            for obj in self.objects:
                obj.y = y
                y -= vspace
    def set_all(self,state=None):
        "Use with Switchball controls,..."
        for obj in self.objects: #visible objects only...
            if hasattr(obj,update):
                obj.update(state)
        
    def select(self,item): 
        """ Radio button mode, for use with control objects like SwitchBall
        ...only one selection at a time.
        """
        self.set_all(False)
        if item in self.objects and hasattr(item,'update'):
            item.update(True)

class hplot(Frame): 
    """Create an x-y plot, where the horizontal axis x is the independent variable, and provide for
    animating it.  This derives from
    my VPyTools.Frame so it inherits show() and animate() methods from there, and the objects list
    and the independent coordinate reference (modifying (x,y,z) moves the whole frame w.r,t the caller)
    from visual.frame.  xax and yax are pairs with the x and y axis endpoints.  The axes
    intersect at (0,0).  Any extra keyword
    arguments provided go to frame (e.g., y=...).  Should work as a vertical plot just by providing
    axis=(0,1,0)?

    The function represented on the y axis is defined by the bound function shape(), which is called
    with the internal curve object (self.data) and any motion variables.  For example, to make a sine wave:
        plot=hplot()
        hplot.shape = lambda o,t : sin(pi*o.x + t)
    and then the curve can be animated by the call:
        plot.animate(t)
    """
    def __init__(self, xax=None, yax=None, text='Plot',color=color.cyan, 
        points=20, radius=0.03, tics=0, **args):
        Frame.__init__(self,**args) #pass remaining keyword args to visual.frame()
        if xax is None:
            xax=(0,1)
        if yax is None:
            yax=(0,1)
        self.xaxis = curve(pos=[(xax[0],0),(xax[1],0)], frame=self, radius=radius)
        self.yaxis = curve(pos=[(xax[0],yax[0]),(xax[0],yax[1])], frame=self, radius=radius)
        self.label = Label(pos=(xax[0],(yax[0]+yax[1])/2),text=text,height = 16, line=0, frame=self)
        self.label.xoffset = -len(text)*self.label.height/8
        if tics > 0 :
            lengthtics = (yax[1]-yax[0])/20.
            ticlabeloffset = -lengthtics-.25  # if this gives me any trouble, pass it through from the call.
            self.ticmarks = []
            self.ticlabels = []
            for xx in range (1,tics+1):
                self.ticmarks.append(curve(pos=[(xx,-lengthtics/2),(xx,lengthtics/2)], radius=radius, frame=self))
                self.ticlabels.append(Label(pos=(xx,ticlabeloffset),text=str(xx),height=16,line=0,frame=self))
        step = (xax[1]-xax[0])/(points-1)
        self.data = curve(x=arange(xax[0],xax[1]+step/2,step), color=color, frame=self, radius=radius)
    def animate(self,*vals):
        self.data.y = self.shape(self.data, *vals)
    def shape(self,o,*vals):
        print 'shape function still undefined for',self.__class__

class vplot(Frame):
    """Similar to hplot, but y is the independent variable
    and the x values are recalculated during animation.
    Also tic marks every 1.000 on the y axis are an option."""
    def __init__(self, xax=(0,1), yax=(0,1), text='Plot',color=color.cyan, points=20,
                radius=0.03, tics=0, **args):
        Frame.__init__(self,**args) #pass remaining keyword args to visual.frame()
        self.xaxis = curve(pos=[(xax[0],0),(xax[1],0)], radius=radius, frame=self)
        self.yaxis = curve(pos=[(0,yax[0]),(0,yax[1])], radius=radius, frame=self)
        self.label = Label(pos=(0,yax[1]),text=text,height = 16, line=0, frame=self)
        self.label.xoffset = -len(text)*self.label.height/8
        if tics > 0 :
            lengthtics = (xax[1]-xax[0])/20.
            ticlabeloffset = -lengthtics-.1  # if this gives me any trouble, pass it through from the call.
            self.ticmarks = []
            self.ticlabels = []
            for yy in range (1,tics+1):
                self.ticmarks.append(curve(pos=[(-lengthtics/2,yy),(lengthtics/2,yy)], radius=radius, frame=self))
                self.ticlabels.append(Label(pos=(ticlabeloffset,yy),text=str(yy),height=16,line=0,frame=self))
        step = (yax[1]-yax[0])/(points-1)
        self.data = curve(y=arange(yax[0],yax[1]+step/2,step), color=color, radius=radius, frame=self)
    def animate(self,*vals):
        self.data.x = self.shape(self.data, *vals)
    def shape(self,o,*vals):
        print 'shape function still undefined for',self.__class__

class xplanes(Frame):
    """Similar to hplot, this creates a series of vertical lines along a horizontal axis.
    The axis endpoints are the pair xax.  shape() defines the x motion of each plane about
    its initial point (plane.x0).
    """
    def __init__(self, xax=None,height=1.0,width=1.0,color=color.cyan, 
        planes=10, radius=0.03, **args):
        Frame.__init__(self,**args)
        if xax is None:
            xax=(0,1)
        step = (xax[1]-xax[0])/(planes-1)
        for x in arange(xax[0],xax[1]+step,step):
            vertline = curve(pos=[(x,-height/2),(x,height/2)],color=color, 
                radius=radius, frame=self)
            vertline.x0 = x
    def animate(self,*vals):
        for o in self.objects:
            o.x = self.shape(o, *vals)
    def shape(self,o,*vals):
        print 'shape function still undefined for',self.__class__

class yplanes(Frame):
    """Similar to xplanes, cloned by Greg
    """
    def __init__(self, yax=None,length=1.0,width=1.0,color=color.cyan, 
        planes=10, radius=0.03, **args):
        Frame.__init__(self,**args)
        if yax is None:
            yax=(0,1)
        step = (yax[1]-yax[0])/(planes-1)
        for y in arange(yax[0],yax[1]+step,step):
            horline = curve(pos=[(-length/2,y),(length/2,y)],color=color, 
                radius=radius, frame=self)
            horline.y0 = 7
    def animate(self,*vals):
        for o in self.objects:
            o.y = self.shape(o, *vals)
    def shape(self,o,*vals):
        print 'shape function still undefined for',self.__class__

def arc(xcen,ycen,radius,thetaI,thetaF): #a list of (x,y) points, going ccw
    if thetaI > thetaF: thetaF = thetaF + 360
    thetaStart=thetaI*pi/180
    thetaEnd=thetaF*pi/180
    step = (thetaEnd-thetaStart)/int((thetaEnd-thetaStart)/(pi/24))
    arc = []
    for i in arange(thetaStart, thetaEnd+0.001, step):
        arc.append((xcen+radius*cos(i), ycen+radius*sin(i), 0))
    return arc

def caller():
    """ Find out how the op sys started the run.
    sys.argv is a list, showing how the program was called from op sys. 
    Usually, sys.argv is a one-member list.
    This list will have more than one member if a "blank, option" was
    typed after the program name.  e.g.
    "MyProgram /option"
    will yield 
    sys.argv = [ path\\MyProgram,  /option ]

    I will allow for one or two members, and make it case-insensitive.
        If two members, the 2nd member is the option.  Strip /, \, and -.
    """
    import sys
#    print 'sys.argv =', sys.argv # comment out when done
    if len(sys.argv) > 1: # programName, blank, option:
        aniName = sys.argv[0].split('\\')[-1].replace(' ','').lower()
        myOption = sys.argv[1].replace('-','').replace('\\','').replace('/','').lower()
    else: # programName-option.  Or, no option
        myList = sys.argv[0].split('\\')[-1].replace('_','-').lower().split('-')
        if len(myList) > 1: 
            aniName = myList[-2].split('\\')[-1].replace(' ','')
            myOption = myList[-1].split('.')[0]
        else: # no option:
            aniName = myList[-1].split('\\')[-1].replace(' ','')
            myOption = "none"
    aniName = aniName.split('.')[0]
#    print 'aniName =', aniName # comment out when done
#    print 'myOption =', myOption # comment out when done
    return [aniName,myOption]
        
class Display(display):
    def __init__(self, **args):
        display.__init__(self, **args)
        self.x = 15;  self.y = 4
##        self.width = 1200;  self.height = 985  # for my PC and projectors, 1200 x 985 
        self.width = 1000;  self.height = 768  # for DLG's PC.
#       the build option in Label also needs to be changed.
        self.fov = 0.05
        self.lights = [vector(0,0,1)]
        self.ambient = 0.5  #this brightens tipped arrow heads.
#  The small fov makes 3-d "arrows" appear flat. Lights keeps the arrow 
#   heads lit almost as well as the shafts.  
##        self.fullscreen = True

class Label(label):
    def __init__(self, **args):
        label.__init__(self, **args)
        self.box = 0
##        self.height = 28 # 25 or 28.  28 for mine, and for PASS.  
        self.height = 20 
#       the build option in Display also needs to be changed.
        self.opacity = 0

