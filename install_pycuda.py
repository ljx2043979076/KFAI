"""
自动安装 PyCUDA 的脚本
尝试多种方法安装 PyCUDA,直到成功为止
"""
import subprocess
import sys
import os
import urllib.request
import tempfile

def run_command(cmd):
    """运行命令并返回是否成功"""
    try:
        print(f"\n正在执行: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"执行失败: {e}")
        return False

def try_conda_forge():
    """尝试使用 conda-forge 安装"""
    print("\n=== 方法1: 尝试使用 conda-forge 安装 PyCUDA ===")
    
    # 检查是否有 conda
    if run_command(["conda", "--version"]):
        return run_command(["conda", "install", "-c", "conda-forge", "pycuda", "-y"])
    
    print("未检测到 conda")
    return False

def try_prebuilt_wheel():
    """尝试从各种源下载预编译 wheel"""
    print("\n=== 方法2: 尝试下载预编译 wheel ===")
    
    # 可能的 wheel 下载链接 (Python 3.10, Windows AMD64)
    wheel_urls = [
        "https://github.com/conda-forge/pycuda-feedstock/releases/latest",
        # 可以添加其他可能的链接
    ]
    
    python_exe = sys.executable
    
    for url in wheel_urls:
        print(f"\n尝试从 {url} 下载...")
        try:
            # 这里需要手动找到实际的 wheel 文件 URL
            print("需要手动下载 wheel 文件")
        except Exception as e:
            print(f"下载失败: {e}")
    
    return False

def install_build_tools():
    """提示安装编译工具"""
    print("\n=== 方法3: 从源码编译 (需要 Visual Studio Build Tools) ===")
    print("\n要从源码编译 PyCUDA,你需要:")
    print("1. 安装 Microsoft Visual C++ Build Tools")
    print("   下载地址: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
    print("2. 安装时选择 'Desktop development with C++' workload")
    print("3. 确保 CUDA Toolkit 已正确安装")
    print("\n安装完成后,运行以下命令:")
    print(f"  {sys.executable} -m pip install pycuda")
    
    response = input("\n是否已经安装了 Visual Studio Build Tools? (y/n): ").lower()
    if response == 'y':
        return run_command([sys.executable, "-m", "pip", "install", "pycuda"])
    
    return False

def check_cuda_installation():
    """检查 CUDA 是否已安装"""
    print("\n=== 检查 CUDA 环境 ===")
    
    cuda_path = os.environ.get('CUDA_PATH')
    if cuda_path:
        print(f"检测到 CUDA_PATH: {cuda_path}")
        nvcc_path = os.path.join(cuda_path, 'bin', 'nvcc.exe')
        if os.path.exists(nvcc_path):
            print(f"找到 nvcc: {nvcc_path}")
            run_command([nvcc_path, "--version"])
            return True
    else:
        print("未检测到 CUDA_PATH 环境变量")
    
    # 尝试查找 nvcc
    if run_command(["where", "nvcc"]):
        return True
    
    print("\n警告: 未检测到 CUDA Toolkit")
    print("请从以下地址下载并安装 CUDA Toolkit:")
    print("https://developer.nvidia.com/cuda-downloads")
    
    return False

def main():
    print("=" * 70)
    print("PyCUDA 自动安装脚本")
    print("=" * 70)
    
    # 检查当前 Python 版本
    print(f"\nPython 版本: {sys.version}")
    print(f"Python 路径: {sys.executable}")
    
    # 检查 CUDA
    has_cuda = check_cuda_installation()
    if not has_cuda:
        print("\n建议: 先安装 CUDA Toolkit 再安装 PyCUDA")
        response = input("是否继续尝试安装 PyCUDA? (y/n): ").lower()
        if response != 'y':
            return
    
    # 尝试各种安装方法
    methods = [
        try_conda_forge,
        try_prebuilt_wheel,
        install_build_tools,
    ]
    
    for i, method in enumerate(methods, 1):
        print(f"\n{'=' * 70}")
        print(f"尝试方法 {i}/{len(methods)}")
        print(f"{'=' * 70}")
        
        if method():
            print("\n" + "=" * 70)
            print("✅ PyCUDA 安装成功!")
            print("=" * 70)
            
            # 验证安装
            print("\n正在验证安装...")
            try:
                import pycuda
                import pycuda.driver as cuda
                print(f"PyCUDA 版本: {pycuda.VERSION_TEXT}")
                print("✅ PyCUDA 导入成功!")
                return
            except Exception as e:
                print(f"❌ PyCUDA 导入失败: {e}")
                return
        
        print(f"\n方法 {i} 失败,尝试下一个方法...")
    
    print("\n" + "=" * 70)
    print("❌ 所有自动安装方法均失败")
    print("=" * 70)
    print("\n建议:")
    print("1. 手动下载 PyCUDA wheel 文件并安装")
    print("2. 或者安装 Visual Studio Build Tools 后从源码编译")
    print("3. 或者联系技术支持获取帮助")

if __name__ == "__main__":
    main()
