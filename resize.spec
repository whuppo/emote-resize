# -*- mode: python -*-

block_cipher = None


a = Analysis(['resize.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

a.datas += [('resize.png','resize.png', 'Data')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          Tree( 'tkdnd2.9.2', prefix='tkdnd2.9.2\\' ),
          Tree( 'TkinterDnD2', prefix='TkinterDnD2\\' ),
          a.zipfiles,
          a.datas,
          [],
          name='resize',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='resize.ico' )
