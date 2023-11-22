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
    lib_file_prefix = ""

    if args.platform == "windows":
        cmake_args.extend(["-G", f"Visual Studio {args.vs_version} {'2019' if args.vs_version == 16 else '2022'}"])
        lib_file_extension = ".lib"
        lib_file_name = "marl"
        lib_file_path = f"{build_dir}/{'Debug' if args.config == 'debug' else 'Release'}/{lib_file_name}{lib_file_extension}"
        lib_file_prefix = ""
    elif args.platform == "macos":
        cmake_args.extend(["-G", "Xcode"])
        lib_file_extension = ".a"  # Change this to ".dylib" for dynamic libraries
        lib_file_name = "libmarl"
        lib_file_path = f"{build_dir}/{'Debug' if args.config == 'debug' else 'Release'}/{lib_file_name}{lib_file_extension}"
        lib_file_prefix = "lib"
    elif args.platform == "android":
        cmake_args.extend([
            "-G", "Unix Makefiles",
            f"-DCMAKE_TOOLCHAIN_FILE:PATH={os.environ['ANDROID_NDK_ROOT']}/build/cmake/android.toolchain.cmake",
            f"-DANDROID_ABI={args.arch}",
            f"-DANDROID_NATIVE_API_LEVEL={str(args.android_api_level)}"
        ])
        lib_file_extension = ".a"
        lib_file_name = "libmarl"
        lib_file_path = f"{build_dir}/{lib_file_name}{lib_file_extension}"
        lib_file_prefix = "lib"
    elif args.platform == "ios":
        cmake_arg_arch = "OS64COMBINED" if (args.arch == "x86_64") else "OS"
        cmake_args.extend(["-G", "Xcode"])
        cmake_args.extend([
            f"-DCMAKE_TOOLCHAIN_FILE:PATH={project_root}/submodules/ios-cmake/ios.toolchain.cmake",
            f"-DPLATFORM={cmake_arg_arch}"
        ])
        lib_file_extension = ".a"  # Change this to ".dylib" for dynamic libraries
        lib_file_name = "libmarl"
        lib_file_path = f"{build_dir}/{'Debug-iphoneos' if args.config == 'debug' else 'Release-iphoneos'}/{lib_file_name}{lib_file_extension}"
        lib_file_prefix = "lib"

    cmake_args.append("-DCMAKE_BUILD_TYPE=" + args.config)

    os.makedirs(build_dir, exist_ok=True)
    subprocess.check_call(cmake_args, cwd=build_dir)

    # Build the generated solution
    build_args = ["cmake", "--build", build_dir, "--config", "Debug" if args.config == "debug" else "Release"]
    subprocess.check_call(build_args)
    
    return {
        "project_root": project_root,
        "lib_file_path": lib_file_path,
        "include_dir": f"{project_root}/include",
        "src_dir": f"{project_root}/src",
        "lib_file_extension": lib_file_extension,
        "lib_file_prefix": lib_file_prefix
    }

def export_project(build_info, args):
    export_dir = f"{build_info['project_root']}/build/export/libs/{args.config}"
    
    # Create directories if they do not exist
    os.makedirs(export_dir, exist_ok=True)
    
    export_file_path = f"{export_dir}/marl.{args.platform}.{args.arch}{build_info['lib_file_extension']}"
    
    shutil.copy(build_info["lib_file_path"], export_file_path)
    
    # Copy include directory
    shutil.copytree(build_info["include_dir"], f"{build_info['project_root']}/build/export/include", dirs_exist_ok=True)
    
    # Copy src directory
    shutil.copytree(build_info["src_dir"], f"{build_info['project_root']}/build/export/src", dirs_exist_ok=True)

def get_godot_platform_name(platform):
    if args.platform == "windows":
        return "windows"
    elif args.platform == "macos":
        return "macos"
    elif args.platform == "android":
        return "android"
    elif args.platform == "ios":
        return "ios"

def get_godot_arch_name(arch):
    if args.arch == "x86":
        return "x86"
    elif args.arch == "x86_64":
        return "x86_64"
    elif args.arch == "armeabi-v7a":
        return "arm32"
    elif args.arch == "arm64-v8a":
        return "arm64"

def get_godot_config_name(config):
    if args.config == "debug":
        return "template_debug"
    elif args.config == "release":
        return "template_release"

def export_godot_compatible_lib(build_info, args):
    export_dir = f"{build_info['project_root']}/build/export/gdcompatible_libs"
    
    # Create directories if they do not exist
    os.makedirs(export_dir, exist_ok=True)

    # prepare args
    platform = get_godot_platform_name(args.platform);
    arch = get_godot_arch_name(args.arch);
    config = get_godot_config_name(args.arch);

    # file
    lib_file_prefix = build_info['lib_file_prefix']
    lib_file_extension = build_info['lib_file_extension']

    # copy files
    shutil.copy(
        build_info["lib_file_path"], 
        f"{export_dir}/{lib_file_prefix}marl.{platform}.{config}.{arch}{lib_file_extension}"
    )
    if args.config == "release":  
        shutil.copy(
            build_info["lib_file_path"], 
            f"{export_dir}/{lib_file_prefix}marl.{platform}.editor.{arch}{lib_file_extension}"
        )   
        shutil.copy(
            build_info["lib_file_path"], 
            f"{export_dir}/{lib_file_prefix}marl.{platform}.editor.dev.{arch}{lib_file_extension}"
        )
    shutil.copy(
        build_info["lib_file_path"], 
        f"{export_dir}/{lib_file_prefix}marl.{platform}.{config}.dev.{arch}{lib_file_extension}"
    )

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
    export_godot_compatible_lib(build_info, args)
