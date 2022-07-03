# for some reason cannot get compile to run outside of -ti ; get exec format error
# but running within shell works fine ???
# if i install qemu-user-static on the podman machine vm, i lose mounts
# apparently have to be specific about those, too, e.g. machine init -v $HOME:$HOME
podman run --platform linux/arm64 --mount type=bind,source=$(pwd),destination=/ps4disasm/ --workdir /ps4disasm/ --rm -ti asl /bin/bash

