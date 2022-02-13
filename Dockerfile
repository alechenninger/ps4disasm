FROM registry.redhat.io/ubi8/ubi
RUN yum -y install git gcc make; yum clean all
RUN git clone -b upstream --single-branch https://github.com/Macroassembler-AS/asl-releases.git
RUN cd asl-releases && cp Makefile.def.tmpl Makefile.def && make

