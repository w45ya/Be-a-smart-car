# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\Coding\\Be-a-smart-car'],
             binaries=[],
             datas=[('resources/backgrounds/*','resources/backgrounds'),('resources/font/*','resources/font'),('resources/menu/*','resources/menu'),('resources/sound/*','resources/sound'),('resources/icon/*','resources/icon'),('resources/sprites/*','resources/sprites')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon='D:\\Coding\\Be-a-smart-car\\resources\\icon\\icon.ico')
