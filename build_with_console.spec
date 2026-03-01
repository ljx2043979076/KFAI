# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 配置文件 - 带控制台版本
用于打包成可执行文件,保留控制台窗口以便查看输出和调试
"""

block_cipher = None

# 需要收集的额外数据文件
added_files = [
    ('ChillBitmap_16px.ttf', '.'),  # 字体文件
    ('msyh.ttc', '.'),              # 微软雅黑字体
    ('undefeated.ttf', '.'),        # 字体文件
    ('skeet_gradient.png', '.'),    # 渐变图片
    ('km.dll', '.'),                # KM盒子DLL
    ('logitech.dll', '.'),          # 罗技DLL
    ('kmNet.cp310-win_amd64.pyd', '.'),  # KMNet模块
    ('pykm2.pyc', '.'),             # KM模块
    ('config.json', '.'),           # 配置文件
    ('cfg.json', '.'),              # 配置文件
]

# 需要导入的隐藏模块
hiddenimports = [
    # 核心依赖
    'core',
    'infer_class',
    'infer_function', 
    'inference_engine',
    'function',
    'gui_handlers',
    'screenshot_manager',
    'profiler',
    'remote_config',
    'server_config',
    'decode_model',
    
    # 第三方库
    'dearpygui',
    'dearpygui.dearpygui',
    'onnxruntime',
    'onnxruntime.capi',
    'cv2',
    'numpy',
    'PIL',
    'PIL.Image',
    'pynput',
    'pynput.keyboard',
    'pynput.mouse',
    'pyclick',
    'pydirectinput',
    'bettercam',
    'kmNet',
    
    # 科学计算
    'scipy',
    'scipy.optimize',
    'filterpy',
    'filterpy.kalman',
    
    # 加密和网络
    'cryptography',
    'cryptography.fernet',
    'requests',
    'websocket',
    
    # Windows相关
    'win32api',
    'win32con',
    'win32gui',
    'ctypes',
    'serial',
    'serial.tools.list_ports',
    
    # 其他
    'queue',
    'threading',
    'concurrent.futures',
    'base64',
    'json',
    'traceback',
]

# 尝试导入TensorRT相关(如果存在)
try:
    import tensorrt
    hiddenimports.extend([
        'tensorrt',
        'pycuda',
        'pycuda.driver',
        'pycuda.autoinit',
    ])
    print("检测到TensorRT,将包含TRT支持")
except ImportError:
    print("未检测到TensorRT,将使用纯ONNX模式")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'pytest',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ZTXAI_Console',  # 可执行文件名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 重要: 设置为True以显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以指定图标文件路径
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ZTXAI_Console',  # 输出文件夹名称
)
