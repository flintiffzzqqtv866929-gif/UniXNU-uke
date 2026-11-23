/*
 * The GPU addon staging counters.
 *
 * On the macOS profiles scripts/make-gpu-addon.py's image is staged by
 * zzy-native-gpu-addon-mount.patch, which owns these globals in bsd/kern/kern_exec.c. The 24A446 OS
 * series carries no such patch, yet the display probe (package/GpuPowerProbe.cpp) and the last-log
 * writer (kits/uke/UkeLastLog.cpp of ShengUfs) still read them, so the kernel link needs a definition.
 * They stay inert: files is -1, the "not staged" value the probe tests before it logs a result, and no
 * kernel code writes them on this profile.
 */
volatile int native_gpu_addon_stage = 0;
volatile int native_gpu_addon_status = 0;
volatile int native_gpu_addon2_stage = 0;
volatile int native_gpu_addon2_status = 0;
volatile int native_gpu_addon_files = -1;
volatile int native_gpu_addon_written = 0;
volatile int native_gpu_addon_same = 0;
volatile int native_gpu_addon_failed = 0;
volatile int native_gpu_addon_error = 0;
volatile int native_gpu_addon_released = 0;
