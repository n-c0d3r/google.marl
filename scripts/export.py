"""
This script builds a CMake project at /project_root/
CLI Arguments:
    --platform: windows|macos|android (default=windows)
    --arch: x86|x86_64|arm64-v8a|armeabi-v7a (default=x86_64)
    --android_api_level: ... (default=24)
    --config: debug|release (default=debug)
    --vs_version: 16|17 (default=17)
"""

import os
import argparse
import subprocess
import shutil

def build_cmake_project(args):
    # Get the path of this script
    script_path = os.path.realpath(__file__)
    # Get the project root directory (assuming the script is in /project_root/scripts/)
    project_root = os.path.dirname(os.path.dirname(script_path))

    # Build dir and source dir
    build_dir = f"{project_root}/build/{args.platform}/{args.arch}/{args.config}"
    cmake_args = ["cmake", "-B", build_dir, "-S", project_root]

    # Lib file ex, name, path
    lib_file_extension = ""
    lib_file_name = ""
    lib_file_path = ""

    if args.platform == "windows":
        cmake_args.extend(["-G", f"Visual Studio {args.vs_version} {'2019' if args.vs_version == 16 else '2022'}"])
        lib_file_extension = ".lib"
        lib_file_name = "marl"
        lib_file_path = f"{build_dir}/{'Debug' if args.config == 'debug' else 'Release'}/{lib_file_name}{lib_file_extension}"
    elif args.platform == "macos":
        cmake_args.extend(["-G", "Xcode"])
        lib_file_extension = ".a"  # Change this to ".dylib" for dynamic libraries
        lib_file_name = "libmarl"
        lib_file_path = f"{build_dir}/{lib_file_name}{lib_file_extension}"
    elif args.platform == "android":
        cmake_args.extend([
            "-G", "Unix Makefiles",
            "-DCMAKE_TOOLCHAIN_FILE:PATH=" + os.environ['ANDROID_NDK_ROOT'] + "/build/cmake/android.toolchain.cmake",
            "-DANDROID_ABI=" + args.arch,
            "-DANDROID_NATIVE_API_LEVEL=" + str(args.android_api_level)
        ])
        lib_file_extension = ".a"
        lib_file_name = "libmarl"
        lib_file_path = f"{build_dir}/{lib_file_name}{lib_file_extension}"

    cmake_args.append("-DCMAKE_BUILD_TYPE=" + args.config)

    os.makedirs(build_dir, exist_ok=True)
    subprocess.check_call(cmake_args, cwd=build_dir)

    # Build the generated solution
    build_args = ["cmake", "--build", build_dir, "--config", args.config]
    subprocess.check_call(build_args)
    
    return {
        "project_root": project_root,
        "lib_file_path": lib_file_path,
        "include_dir": f"{project_root}/include",
        "lib_file_extension": lib_file_extension
    }

def export_project(build_info, args):
    export_dir = f"{build_info['project_root']}/build/export/libs/{args.config}"
    
    # Create directories if they do not exist
    os.makedirs(export_dir, exist_ok=True)
    
    export_file_path = f"{export_dir}/marl.{args.platform}.{args.arch}{build_info['lib_file_extension']}"
    
    shutil.copy(build_info["lib_file_path"], export_file_path)
    
    # Copy include directory
    shutil.copytree(build_info["include_dir"], f"{build_info['project_root']}/build/export/include", dirs_exist_ok=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build CMake project.')
    parser.add_argument('--platform', default='windows', help='Platform to build for (windows|macos|android)')
    parser.add_argument('--arch', default='x86_64', help='Architecture to build for (x86|x86_64|arm64-v8a|armeabi-v7a)')
    parser.add_argument('--android_api_level', default=24, type=int, help='Android API level (default=24)')
    parser.add_argument('--config', default='debug', help='Build configuration (debug|release)')
    parser.add_argument('--vs_version', default=17, type=int, help='Visual Studio version (16|17) (default=17)')
    
    args = parser.parse_args()
    
    build_info = build_cmake_project(args)
    
    export_project(build_info, args)
