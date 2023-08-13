FROM registry.redhat.io/ubi8/ubi
RUN yum -y install git gcc make python3; yum clean all

# Compile asl
RUN git clone -b upstream --single-branch https://github.com/Macroassembler-AS/asl-releases.git
# Pin to build 246 for now
# 247 was completely broken; emailed dev
RUN cd asl-releases && git checkout de21deab4251653ab7355315ddb3140c9c2f1743 && cp Makefile.def-samples/Makefile.def-unknown-linux Makefile.def && make clean && make -j8
# -j8 doesn't build docs, but also doesn't install.
# Copying to /usr/bin/ fails, unable to find some message bundles.
# So setting the path works.
ENV PATH="/asl-releases:${PATH}"

# Compile custom p2bin
# Not sure if the asl p2bin can be made to work but :shrug:
ADD AS/ps4p2bin.c /tmp/
RUN gcc -O3 -w -o /usr/bin/ps4p2bin /tmp/ps4p2bin.c
