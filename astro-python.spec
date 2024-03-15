from sys import platform
block_cipher = None

# we need to collect the correct webui lib for the platform we are building for.
# it can be found at .venv/Lib/site-packages/webui/[build-string]/webui-2.[ext]

# only supporting x64 linux/windows
if platform == "linux" or platform == "linux2":
    LIB_STRING = "webui-linux-gcc-x64"
    LIB_EXT = "so"
elif platform == "win32" or platform == "win64":
    LIB_STRING = "webui-windows-msvc-x64"
    LIB_EXT = "dll"
else:
    raise Exception("Unsupported platform")


a = Analysis(['./packages/python-app/main.py'],
             pathex=['./packages/python-app'],
             datas=[
                ('./dist/astro', 'dist/astro'), # astro static files
                (f'./.venv/Lib/site-packages/webui/{LIB_STRING}/webui-2.{LIB_EXT}', f'{LIB_STRING}/')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[
                './packages/python-app/pyinstaller_hooks.py'
             ],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='astro-python',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)  # or False, depending on your need

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='astro-python')
