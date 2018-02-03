# -*- mode: python -*-

block_cipher = None


a = Analysis(['commander/run.py'],
             pathex=['/Users/Andrew/Desktop/Andrew/Drive/2017-2018/sandbox/S2AssistantAssistant', '/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages',],
             binaries=None,
             datas=None,
             hiddenimports=['PyQt5','six','packaging', 'packaging.version', 'appdirs', 'packaging.specifiers', 'pyparsing'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='run.app',
          debug=False,
          strip=False,
          upx=True,
          console=True )