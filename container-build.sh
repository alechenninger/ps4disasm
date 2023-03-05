osascript -e 'display notification "Build starting... ('$1' files changed)" with title "ps4disasm"'
podman run --platform linux/arm64 --mount type=bind,source=$(pwd),destination=/ps4disasm/ --workdir /ps4disasm/ --rm -ti asl /bin/bash -c /ps4disasm/build-all-grand-cross.sh
date
osascript -e 'display notification "Build complete ✅" with title "ps4disasm"'
