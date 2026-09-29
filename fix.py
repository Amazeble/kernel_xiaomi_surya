import re
import os
import shutil

TARGET_FILE = "fs/proc/base.c"
BACKUP_FILE = TARGET_FILE + ".bak_final"  # <-- Added quotes here

def patch_base_c():
    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: {TARGET_FILE} not found.")
        return False
    
    print(f"Patching {TARGET_FILE}...")
    
    # Backup
    if not os.path.exists(BACKUP_FILE):
        shutil.copy2(TARGET_FILE, BACKUP_FILE)
        print(f"  -> Backup created: {BACKUP_FILE}")

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # --- STRATEGY: Replace the conditional include with an unconditional one for KSU_SUSFS ---
    # Current problematic block in base.c:
    # #if defined(CONFIG_KSU_SUSFS_SUS_MAP)|| defined(CONFIG_KSU_SUSFS_OPEN_REDIRECT)
    # #include <linux/susfs_def.h>
    # #endif 
    
    # We want to ensure susfs_def.h is included whenever CONFIG_KSU_SUSFS is active,
    # because susfs_def.h defines SUSFS_IS_INODE_OPEN_REDIRECT which is used in base.c.
    
    pattern_old = r"(#if defined\(CONFIG_KSU_SUSFS_SUS_MAP\)\s*\|\|\s*defined\(CONFIG_KSU_SUSFS_OPEN_REDIRECT\)\s*\n\s*#include <linux/susfs_def\.h>\s*\n\s*#endif // #if defined\(CONFIG_KSU_SUSFS_SUS_MAP\)\s*\|\|\s*defined\(CONFIG_KSU_SUSFS_OPEN_REDIRECT\))"
    
    replacement_new = "#ifdef CONFIG_KSU_SUSFS\n#include <linux/susfs_def.h>\n#endif"

    new_content, count = re.subn(pattern_old, replacement_new, content, count=1)
    
    if count > 0:
        content = new_content
        modified = True
        print("  -> Fix Applied: Changed susfs_def.h include to depend on CONFIG_KSU_SUSFS.")
    else:
        print("  -> WARNING: Pattern not matched. Checking if already fixed...")
        if "#ifdef CONFIG_KSU_SUSFS\n#include <linux/susfs_def.h>" in content:
            print("  -> OK: Already patched.")
        else:
            print("  -> ERROR: Could not find the specific include block to replace.")

    if modified:
        with open(TARGET_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print("\nSUCCESS: fs/proc/base.c updated.")
        print("Next step: rm out/fs/proc/base.o && bash run.sh")
    else:
        print("\nNO CHANGES MADE.")

if __name__ == "__main__":
    patch_base_c()