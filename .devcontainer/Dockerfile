FROM mambaorg/micromamba:2.1.1

COPY --chown=$MAMBA_USER:$MAMBA_USER .devcontainer/environment.yml /tmp/environment.yaml
RUN micromamba install -y -n base -f /tmp/environment.yaml && \
    micromamba clean --all --yes
    
FROM ghcr.io/cascode-labs/viper-osic-docker-analog/osic-docker-analog:v0.2


# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
# COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/

# RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    # && rm -rf /tmp/conda-tmp

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    wget \
    git \
    ngspice \
    libngspice0


#Install all the tools needed!

USER root
RUN mkdir -p /ic_tools
WORKDIR /ic_tools
#MAGIC INSTALL
#magic requirements
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends \
#     magic
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    m4 \
    libx11-dev \
    tcl-dev tk-dev \   
    libcairo2-dev \
    mesa-common-dev libgl-dev libglu1-mesa-dev \
    zlib1g-dev    

# RUN   apt-get install magic

RUN git clone git://opencircuitdesign.com/magic
WORKDIR /ic_tools/magic
RUN ./configure
RUN make
RUN make install
    
#INSTALL OPEN PDKS
RUN mkdir -p /ic_tools/pdks_source
WORKDIR /ic_tools/pdks_source
# RUN apt-get update && apt-get install -y locales
RUN git clone git://opencircuitdesign.com/open_pdks
WORKDIR /ic_tools/pdks_source/open_pdks
RUN ./configure --enable-sky130-pdk --enable-sram-sky130 --with-sky130-variants=all
RUN make
RUN make install 



#conda install!
SHELL ["/bin/bash", "-c"]
RUN mkdir -p /ic_tools 
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /ic_tools/miniconda.sh
RUN bash && bash /ic_tools/miniconda.sh -b -p /ic_tools/miniconda3 
ENV PATH="/ic_tools/miniconda3/bin:${PATH}"
RUN rm /ic_tools/miniconda.sh
# SHELL ["/bin/bash", "-lc"]
# RUN bash source ~/miniconda3/bin/activate
RUN conda init --all
# RUN 
# SHELL ["/bin/bash", "-lc"]

# COPY environment.yml* .devcontainer/environment.yml /tmp/conda-tmp/
# RUN source ~/miniconda3/bin/activate 
# WORKDIR /workspaces/VLSI_Grimoire
WORKDIR /workspaces/VLSI_Grimoire
RUN conda env create -f .devcontainer/environment.yml
#conda activate Grimoire 