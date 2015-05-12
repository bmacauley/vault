# -*- mode: python -*-
a = Analysis(['vault.py'],
             pathex=['/Users/bmacauley/projects/vault'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas = list({tuple(map(str.upper, t)) for t in a.datas})
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='vault',
          debug=False,
          strip=None,
          upx=True,
          console=True )
