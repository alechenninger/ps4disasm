set -e
rm script/*.bin* 2> /dev/null || :
if grep -q 'dialog_uncompresed = 0' ps4.options.asm; then 
  (cd script && ./compress_script.py)
fi
linux_build/build.sh ps4.asm out/ps4-genji.bin
