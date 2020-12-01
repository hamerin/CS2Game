import PyInstaller.__main__ as inst

inst.run([
    'start.py',
    '--onefile',
    '--windowed'
])
