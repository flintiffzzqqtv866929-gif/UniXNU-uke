#!/usr/bin/env python3
"""Run the pinned emit_prelink, and when it refuses the layout print the budget both images bring.

The prelink refuses with "Native code would collide with collection data" when the native __TEXT_EXEC
and __KLD, placed after the last retained kext, cross __DATA. The numbers that decide it are the
segment tables of the native image and of the original collection, so a failed run records them here
instead of leaving the next step to guess. The tool itself is unchanged and its output is untouched.

This file is reached as <tree>/kits/uke/prelink-debug.py, a link to the board package: the tree is two
directories above the link as spelled, never through resolve(), which would land in the board checkout.
"""
import os
import subprocess
import sys
from pathlib import Path

TREE = Path(os.path.abspath(__file__)).parents[2]
KITS = TREE / 'kits' / ('XnuPrelink' if (TREE / 'kits/XnuPrelink').is_dir() else 'NativePrelink')
arguments = sys.argv[1:]
status = subprocess.run([sys.executable, str(KITS / 'emit_prelink.py'), *arguments]).returncode
if status:
    def option(name):
        return Path(arguments[arguments.index(name) + 1]) if name in arguments else None
    try:
        sys.path.insert(0, str(KITS))
        from kc_image import Image
        native = Image(option('--kernel').read_bytes())
        cache = Image(option('--prelinked').read_bytes())
        for label, image in (('native', native), ('collection', cache)):
            print(f'--- {label} segments ---')
            for segment in image.segments:
                print(f"  {segment['name']:<18} va={segment['va']:#x} size={segment['size']:#x} "
                      f"filesize={segment['filesize']:#x}")
        code = next(s for s in cache.segments if s['name'] == '__TEXT_EXEC')
        kld = next(s for s in cache.segments if s['name'] == '__KLD')
        data = next(s for s in cache.segments if s['name'] == '__DATA')
        native_code = next(s for s in native.segments if s['name'] == '__TEXT_EXEC')
        native_kld = next((s['size'] for s in native.segments if s['name'] == '__KLD'), 0)
        print(f"code range {code['va']:#x}..{code['va'] + code['size']:#x}, "
              f"__KLD {kld['va']:#x}+{kld['size']:#x}, __DATA {data['va']:#x}")
        print(f"native __TEXT_EXEC {native_code['size']:#x} + __KLD {native_kld:#x}, "
              f"room to __DATA {data['va'] - code['va']:#x}")
    except Exception as error:  # a diagnostic must never replace the real failure
        print('prelink-debug: diagnostics unavailable:', error)
sys.exit(status)
