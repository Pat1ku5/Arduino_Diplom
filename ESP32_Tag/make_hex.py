Import("env")
import os, subprocess

def make_hex(source, target, env):
    build = env.subst("$BUILD_DIR")
    platform = env.PioPlatform()
    esptool = os.path.join(platform.get_package_dir("tool-esptoolpy"), "esptool.py")
    boot_app0 = os.path.join(platform.get_package_dir("framework-arduinoespressif32"),
                             "tools", "partitions", "boot_app0.bin")
    board = env.BoardConfig()
    out = os.path.join(build, "firmware.hex")
    cmd = [
        env.subst("$PYTHONEXE"), esptool,
        "--chip", board.get("build.mcu", "esp32"),
        "merge_bin", "--format", "hex", "-o", out,
        "--flash_mode", board.get("build.flash_mode", "dio"),
        "--flash_freq", board.get("build.f_flash", "40000000L").replace("000000L", "m"),
        "--flash_size", "4MB",
        "0x1000", os.path.join(build, "bootloader.bin"),
        "0x8000", os.path.join(build, "partitions.bin"),
        "0xe000", boot_app0,
        "0x10000", os.path.join(build, "firmware.bin"),
    ]
    subprocess.check_call(cmd)
    print("HEX file created:", out)

env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", make_hex)
