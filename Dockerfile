from ubuntu:20.10
#dunno if all are needed..you test
RUN apt-get update && apt-get install -y \
	libgtk2.0-dev \
	python3-pip \
	software-properties-common \
        gnupg2 \
        ca-certificates \
	apt-transport-https \
	apt-utils \
	wget \
	git autoconf automake build-essential sudo apt-utils

RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
RUN apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main'
RUN apt-get update && apt-get install -y cmake

RUN pip3 install conan==1.41.0
ENV CONAN_REVISIONS_ENABLED=1 

#create lib
WORKDIR /xgboost
COPY conanfile.py .
RUN conan create . xgboost/release_1.4.0@conan/stable

#create test project
WORKDIR /test
COPY conanfile.txt .
COPY CMakeLists.txt .
RUN wget https://raw.githubusercontent.com/dmlc/xgboost/release_1.4.0/demo/c-api/c-api-demo.c

#build
WORKDIR /test/build
RUN conan install ..
RUN cmake ..
RUN cmake --build . --config Release

#get data
WORKDIR /test/build/data
RUN wget https://raw.githubusercontent.com/dmlc/xgboost/release_1.4.0/demo/data/agaricus.txt.test
RUN wget https://raw.githubusercontent.com/dmlc/xgboost/release_1.4.0/demo/data/agaricus.txt.train

#test
WORKDIR /test/build/bin
RUN export LD_LIBRARY_PATH=/test/build/bin:$LD_LIBRARY_PATH
RUN ./c-api-demo

