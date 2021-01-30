set -e
rm script/*.bin*
(cd script && ./compress_script.py)
linux_build/build.sh ps4.asm out/ps4-genji.bin
