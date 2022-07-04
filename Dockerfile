FROM registry.redhat.io/ubi8/ubi
RUN yum -y install git gcc make python3; yum clean all

# Compile asl
RUN git clone -b upstream --single-branch https://github.com/Macroassembler-AS/asl-releases.git
RUN cd asl-releases && cp Makefile.def.tmpl Makefile.def && make -i install

# Compile custom p2bin
# Not sure if the asl p2bin can be made to work but :shrug:
ADD AS/ps4p2bin.c /tmp/
RUN gcc -O3 -w -o /usr/bin/ps4p2bin /tmp/ps4p2bin.c
