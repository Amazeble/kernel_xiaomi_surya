export PATH=/home/hikari/Clang/clang_aosp_12/bin:$PATH
make ARCH=arm64 O=out CC="clang" \
  CROSS_COMPILE="/home/hikari/Gcc/google_gcc_arm64/bin/aarch64-linux-android-" \
  CROSS_COMPILE_ARM32="/home/hikari/Gcc/google_gcc_arm/bin/arm-linux-androideabi-" \
  CLANG_TRIPLE=aarch64-linux-gnu- LD=ld.lld \
  