#!/bin/bash
set -e

echo "=========================================="
echo "  SUSFS Patch Application Script"
echo "=========================================="

KERNEL_DIR="${1:-.}"
PATCHES_DIR="${2:-./SUSFS_Patches}"

cd "$KERNEL_DIR"

# Detect kernel version
if [ -f "Makefile" ]; then
  KERNEL_VERSION=$(head -n 3 Makefile | grep -E 'VERSION|PATCHLEVEL' | awk '{print $3}' | paste -sd '.')
  echo "📋 Detected kernel version: $KERNEL_VERSION"
else
  echo "❌ Makefile not found in kernel directory"
  exit 1
fi

# Find appropriate SUSFS patch
SUSFS_PATCH=""
if [ -d "$PATCHES_DIR/Patch" ]; then
  for patch_file in "$PATCHES_DIR/Patch"/susfs_patch_to_*.patch; do
    if [ -f "$patch_file" ]; then
      SUSFS_PATCH="$patch_file"
      echo "📦 Found SUSFS patch: $(basename $patch_file)"
      break
    fi
  done
fi

if [ -z "$SUSFS_PATCH" ]; then
  echo "⚠️ No SUSFS patch found, skipping patch application"
  echo "ℹ️ You can manually apply patches from SUSFS_Patches directory"
  exit 0
fi

# Check if already patched
if grep -q "CONFIG_KSU_SUSFS" fs/namespace.c 2>/dev/null; then
  echo "✅ SUSFS appears to be already patched"
  exit 0
fi

# Apply patch
echo "🔨 Applying SUSFS patch..."
if patch -p1 < "$SUSFS_PATCH"; then
  echo "✅ SUSFS patch applied successfully"
else
  echo "⚠️ Some parts of the patch may have failed"
  echo "ℹ️ Check for .rej files and resolve conflicts manually"
  find . -name "*.rej" -type f
fi

echo "=========================================="
echo "  SUSFS Integration Complete"
echo "=========================================="
