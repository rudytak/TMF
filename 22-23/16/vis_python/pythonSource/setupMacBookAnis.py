"""
This is a setup.py script for py2app

Usage:
    python setupMacEtcEtc.py py2app
    Then include the readme, and zip it up.
"""
import shutil, os, os.path
from setuptools import setup

killFolders = ['build','dist']
for folder in killFolders:
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder)
        except:
            pass

theLatest = 'mr7g.py'
APP = 'thermoac.py'
shutil.copyfile(theLatest, APP) # This ensures that the app is named thermoac.


DATA_FILES = []
OPTIONS = {'argv_emulation': True,
           'verbose': False,
           'iconfile':'newIcon.icns'}

setup(
    app=[APP],
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)


os.remove(APP) # This ensures that we'll continue development with theLatest.

os.makedirs("dist/pySource")
pyNames = ['PTR.py', 'standing.py', 'Tashe.py', 'thermal.py',
           'viscous.py', 'wave.py',
           theLatest, 'newIcon.icns',
           'animTools.py', 'inits.py', 'feedbackers.py',
           'setupWinBookAnis.py', 'setupMacBookAnis.py' ]
for pyName in pyNames: shutil.copyfile(pyName, os.path.join('dist/pySource',pyName))

shutil.copyfile('readMe.docx', os.path.join('dist', 'readMe.docx'))
shutil.copyfile('requiredLANLdisclaimer.txt', os.path.join('dist', 'requiredLANLdisclaimer.txt'))
