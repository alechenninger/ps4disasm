set -e
(cd script && ./compress_script.py)
linux_build/build.sh ps4.asm out/ps4-$(date --iso-8601=seconds).bin
