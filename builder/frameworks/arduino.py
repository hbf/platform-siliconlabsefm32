# SPDX-License-Identifier: Apache-2.0
"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

https://github.com/SiliconLabs/arduino
"""

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduino-silabs")
assert isdir(FRAMEWORK_DIR)

variant = board.get("build.variant")
variants_dir = (
    join(env.subst("$PROJECT_DIR"), board.get("build.variants_dir"))
    if board.get("build.variants_dir", "")
    else join(FRAMEWORK_DIR, "variants")
)
VARIANT_DIR = join(variants_dir, variant)

machine_flags = [
    "-mthumb",
    "-mcpu=cortex-m33",
    "-mfpu=fpv5-sp-d16",
    "-mfloat-abi=hard",
    "-mcmse",
]

# check what stack is wanted
wanted_stack = "matter"
stack_includes = []
stack_linkerscript = ""
stack_libs = []

# load generic extra flags from board
env.ProcessFlags(board.get("build.arduino.extra_flags", ""))

cpp_defines = env.Flatten(env.get("CPPDEFINES", []))
if "PIO_FRAMEWORK_ARDUINO_STACK_MATTER" in cpp_defines:
    wanted_stack = "matter"
elif "PIO_FRAMEWORK_ARDUINO_STACK_NONE" in cpp_defines:
    wanted_stack = "none"
elif "PIO_FRAMEWORK_ARDUINO_STACK_BLE_ARDUINO" in cpp_defines:
    wanted_stack = "ble_arduino"
elif "PIO_FRAMEWORK_ARDUINO_STACK_BLE_SILABS" in cpp_defines:
    wanted_stack = "ble_silabs"

if wanted_stack == "matter":
    stack_linkerscript = join(VARIANT_DIR, "matter", "linkerfile.ld")
    env.ProcessFlags(board.get("build.arduino.matter_flags", ""))
    stack_libs.append(File(join(VARIANT_DIR, "matter", "gsdk.a")))
    stack_libs.extend([File(join(VARIANT_DIR, "matter", lib)) for lib in board.get("build.arduino.matter_libs", "").split(" ")])
    # matter include directories are the same for all variants, no need to store them in the board file
    stack_includes = [
        join(VARIANT_DIR, "matter"),
        join(VARIANT_DIR, "matter", "autogen", "zap-generated"),
        join(VARIANT_DIR, "matter", "autogen", "zap-generated", "app"),
        join(VARIANT_DIR, "matter", "config"),
        join(VARIANT_DIR, "matter", "config", "btconf"),
        join(VARIANT_DIR, "matter", "config", "common"),
        join(VARIANT_DIR, "matter", "autogen"),
        join(VARIANT_DIR, "matter", "include"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "examples", "platform", "silabs"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "include"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "lib"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "third_party", "nlassert", "repo", "include"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "third_party", "nlio", "repo", "include"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "zzz_generated", "app-common"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "slc", "inc"),
        # join(VARIANT_DIR, "matter", "matter_2.2.0", "examples", "platform", "silabs", "efr32"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "platform", "silabs", "efr32"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "examples", "providers"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "basic-information"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "color-control-server"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "diagnostic-logs-server"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "door-lock-server"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "general-commissioning-server"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "general-diagnostics-server"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "groups-server"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "identify-server"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "level-control"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "network-commissioning"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "occupancy-sensor-server"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "on-off-server"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "ota-requestor"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "third_party", "silabs", "gecko_sdk", "util", "third_party", "segger", "systemview", "SEGGER"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "software-diagnostics-server"),
        join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "switch-server"),
        # join(VARIANT_DIR, "matter", "matter_2.2.0", "src", "app", "clusters", "window-covering-server"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "Device", "SiliconLabs", "MGM24", "Include"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "app", "common", "util", "app_assert"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "app", "common", "util", "app_log"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "common", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "protocol", "bluetooth", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "protocol", "bluetooth", "bgstack", "ll", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "hardware", "board", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "bootloader"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "bootloader", "api"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "CMSIS", "Core", "Include"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "CMSIS", "RTOS2", "Include"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "hardware", "driver", "configuration_over_swo", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "driver", "debug", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "service", "device_init", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "emdrv", "dmadrv", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "emdrv", "common", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "emlib", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "plugin", "fem_util"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "freertos", "cmsis", "Include"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "freertos", "kernel", "include"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "freertos", "kernel", "portable", "GCC", "ARM_CM33_NTZ", "non_secure"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "emdrv", "gpiointerrupt", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "service", "hfxo_manager", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "driver", "i2cspm", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "service", "iostream", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "driver", "leddrv", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "security", "sl_component", "sl_mbedtls_support", "config"),
        # join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "security", "sl_component", "sl_mbedtls_support", "config", "preset"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "security", "sl_component", "sl_mbedtls_support", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "mbedtls", "include"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "mbedtls", "library"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "service", "mpu", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "emdrv", "nvm3", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "openthread", "include"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "openthread", "include", "openthread"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "openthread", "src", "core"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "openthread", "third_party", "tcplp"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "openthread", "examples", "platforms"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "third_party", "openthread", "examples", "platforms", "utils"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "protocol", "openthread", "platform-abstraction", "efr32"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "protocol", "openthread", "platform-abstraction", "include"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "peripheral", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "service", "power_manager", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "security", "sl_component", "sl_psa_driver", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "driver", "pwm", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "common"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "protocol", "ble"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "protocol", "ieee802154"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "protocol", "wmbus"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "protocol", "zwave"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "chip", "efr32", "efr32xg2x"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "protocol", "sidewalk"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "plugin", "pa-conversions"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "plugin", "pa-conversions", "efr32xg24"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "plugin", "rail_util_power_manager_init"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "plugin", "rail_util_pti"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "radio", "rail_lib", "plugin", "rail_util_rssi"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "security", "sl_component", "se_manager", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "security", "sl_component", "se_manager", "src"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "plugin", "security_manager"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "util", "silicon_labs", "silabs_core", "memory_manager"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "common", "toolchain", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "service", "system", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "service", "sleeptimer", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "security", "sl_component", "sl_protocol_crypto", "src"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "emdrv", "spidrv", "inc"),
        join(VARIANT_DIR, "matter", "gecko_sdk_4.4.0", "platform", "service", "udelay", "inc"),
    ]


env.Append(
    ASFLAGS=[],
    ASPPFLAGS=[
        "-x", "assembler-with-cpp",
    ],

    CFLAGS=[
        "-std=gnu11",
    ],

    CCFLAGS=machine_flags + [
        "-Os",  # optimize for size
        "-Wall",  # show warnings
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-fomit-frame-pointer",
        "-imacros",
        "sl_gcc_preinclude.h",
        "-Wno-deprecated-declarations",
        "-Wno-maybe-uninitialized",
        "-Wno-missing-field-initializers",
        "-Wno-unused-parameter",
        "-Wno-cast-function-type",
        "-Wno-psabi",
        "-fno-strict-aliasing",
        "-fno-unwind-tables",
        "-fno-asynchronous-unwind-tables",
        "-fno-common",
        "-Wno-sign-compare"
    ],

    CXXFLAGS=[
        "-std=gnu++17",
        "-fno-exceptions",
    ],

    LINKFLAGS=machine_flags + [
        "-Os",
        "--specs=nano.specs",
        "--specs=nosys.specs",
        "-Wl,--wrap=malloc",
        "-Wl,--wrap=free",
        "-Wl,--wrap=realloc",
        "-Wl,--wrap=calloc",
        "-Wl,--wrap=MemoryAlloc",
        "-Wl,--wrap=_malloc_r",
        "-Wl,--wrap=_realloc_r",
        "-Wl,--wrap=_free_r",
        "-Wl,--wrap=_calloc_r",
        "-Wl,--gc-sections",
        "-Wl,--no-warn-rwx-segments",
        '-Wl,-Map="%s"' % join("${BUILD_DIR}", "${PROGNAME}.map"),
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU"),
        ("ARDUINO", 10808),
        ("ARDUINO_SILABS", env.StringifyMacro("2.2.0")),
        "ARDUINO_ARCH_SILABS",
    ],

    LIBS=[
        "stdc++",
        "gcc",
        "c",
        "m",
    ] + stack_libs,

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", "silabs"),
        join(FRAMEWORK_DIR, "cores", "silabs", "api", "deprecated"),
    ] + stack_includes
)

# Framework requires all symbols from mbed libraries
#env.Prepend(_LIBFLAGS="-Wl,--whole-archive ")
#env.Append(_LIBFLAGS=" -Wl,--no-whole-archive -lstdc++ -lm -lc -lgcc -lnosys")

if not board.get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH=stack_linkerscript)

#
# Target: Build Core Library
#

libs = []

if "build.variant" in board:
    env.Prepend(CPPPATH=[
        VARIANT_DIR
    ])

    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "FrameworkArduinoVariant"),
            VARIANT_DIR))

libs.append(
    env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduino"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"))))

env.Prepend(LIBS=libs)
