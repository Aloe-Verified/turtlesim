FROM osrf/ros:noetic-desktop-full

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    && apt-get clean

RUN pip3 install --no-cache-dir \
    tensorflow \
    keras \
    stable-baselines3 \
    matplotlib \
    gym \
    numpy \
    pandas

RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc

CMD ["bash"]
