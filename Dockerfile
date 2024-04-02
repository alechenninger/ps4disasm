FROM registry.redhat.io/ubi8/ubi
RUN yum -y install git gcc make python3 unzip cmake; yum clean all

# Compile asl from latest sources
ADD http://john.ccac.rwth-aachen.de:8000/ftp/as/source/c_version/asl-current.tar.gz /
RUN tar -xzvf asl-current.tar.gz
RUN cd asl-current && cp Makefile.def-samples/Makefile.def-unknown-linux Makefile.def && make clean && make -j8
# -j8 doesn't build docs, but also doesn't install.
# Copying to /usr/bin/ fails, unable to find some message bundles.
# So setting the path works.
ENV PATH="/asl-current:${PATH}"

# Compile custom p2bin
# Not sure if the asl p2bin can be made to work but :shrug:
ADD AS/ps4p2bin.c /tmp/
RUN gcc -O3 -w -o /usr/bin/ps4p2bin /tmp/ps4p2bin.c

# Compile kcompress
RUN mkdir /kosinski
ADD https://github.com/VanderCat/accurate-kosinski/archive/refs/heads/master.zip /kosinski/
RUN unzip /kosinski/master.zip -d /kosinski/ && \
	rm /kosinski/master.zip
RUN mkdir /kosinski/accurate-kosinski-master/build && cd /kosinski/accurate-kosinski-master/build && cmake /kosinski/accurate-kosinski-master && cmake --build /kosinski/accurate-kosinski-master/build --config Release
ENV PATH="/kosinski/accurate-kosinski-master/build:${PATH}"

