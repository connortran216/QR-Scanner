FROM python:3.6

ARG CAMERA_RTSP_URL
ARG QT_DEBUG_PLUGINS

ENV CAMERA_RTSP_URL=${CAMERA_RTSP_URL}
ENV QT_DEBUG_PLUGINS=${QT_DEBUG_PLUGINS}

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
	tk-dev apt-utils python3-pip tzdata locales

# create alias
RUN cd /usr/bin \
  && ln -sf python3 python \
  && ln -sf pip3 pip

RUN locale-gen en_US.UTF-8

# set locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV TZ=Asia/Ho_Chi_Minh

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get install -y build-essential software-properties-common gcc g++ musl-dev libsm6 libxext6 libxrender-dev
RUN apt install -y libgl1-mesa-glx
RUN apt-get install ffmpeg libsm6 libxext6  -y


COPY . /app
ADD ./requirements.txt requirements.txt
ENV PYTHONPATH=/app

RUN pip install --upgrade pip
RUN pip install grpcio==1.22.0 grpcio-tools==1.22.0
RUN pip install scikit-build
RUN pip install cmake
RUN pip install python-multipart
RUN pip install uvicorn
RUN pip install fastapi
RUN pip install requests
#RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
EXPOSE 8200
#CMD [ "python", "receive_api.py" ]
