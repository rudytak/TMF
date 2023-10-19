"""  2014, make bookAnis folder in Windows,
     for public distribution for my thermoacoustics book.
     To use this, type "setupwinbookanis.py py2exe" in a cmd box.
     This version includes the master mouse-selectable program and its icon.
"""

from distutils.core import setup
import py2exe
import os, os.path, shutil

distFolder = "bookAnis\EXEs"

killFolders = ['build', distFolder]
for folder in killFolders:
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder) # wipe out the "build" and "dist" folders
        except:                     #  in case I've scrambled time-stamp orders.
             pass
            
includes = []
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter' ]
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll','w9xpopen.exe']

Data_Files = []

opts = {
    "py2exe": {"compressed": 2, 
               "optimize": 2,
               "includes": includes,
               "excludes": excludes,
               "packages": packages,
               "dll_excludes": dll_excludes,
               "bundle_files": 2, 
               "xref": False,
               "skip_archive": False,
               "dist_dir": distFolder,
                "ascii": True,
                "custom_boot_script": '',
                }
}

bookAnis = ["PTR.py", "standing.py", "Tashe.py", "thermal.py",
            "viscous.py", "wave.py"]

masterApp = "mr7g.py"
bookAnisWithMaster = bookAnis[:]
bookAnisWithMaster.append( {"script": masterApp,
                            "dest_base": "ThermoAc" }  )
setup(
   options = opts,
   data_files = Data_Files,
   console = bookAnisWithMaster
)

# Cmd users and shortcuts will expect to see oscwall.exe too:
shutil.copyfile(os.path.join("bookanis\EXEs", "viscous.exe"), os.path.join("bookanis\EXEs", "oscwall.exe"))

# Copy the py source files to their distribution folder:
for animName in bookAnis: shutil.copyfile(animName, os.path.join("bookanis\pythonSource",animName))
extras = ["animTools.py", "inits.py", "feedbackers.py",
          masterApp, "setupWinBookAnis.py", "setupMacBookAnis.py" ]
for pyName in extras:     shutil.copyfile(pyName, os.path.join("bookanis\pythonSource",pyName))
