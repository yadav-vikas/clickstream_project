FROM jupyter/pyspark-notebook:latest

USER root

# Install Hadoop
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk wget && \
    wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -xzf hadoop-3.3.6.tar.gz -C /usr/local && \
    ln -s /usr/local/hadoop-3.3.6 /usr/local/hadoop

ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin

USER jovyan
