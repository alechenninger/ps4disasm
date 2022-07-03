set -e
rm script/*.bin* 2> /dev/null || :
if grep -q 'dialog_uncompresed = 0' ps4.options.asm; then 
  (cd script && ./compress_script.py)
fi
# for compat with podman on m1
# forces p2bin to not be on mounted volume to workaround
# https://github.com/containers/podman/issues/14142
linux_build/build.sh --p2bin /tmp/p2bin ps4.asm out/ps4-grand-cross.bin
#linux_build/build.sh ps4.asm out/ps4-grand-cross.bin
