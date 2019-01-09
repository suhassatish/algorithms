FROM centos/python-36-centos7

USER root

RUN yum install -y \
       java-1.8.0-openjdk \
       java-1.8.0-openjdk-devel \
       wget

ENV JAVA_HOME /etc/alternatives/jre

# Spark
RUN cd /usr/ \
&& wget "http://ftp.heanet.ie/mirrors/www.apache.org/dist/spark/spark-2.3.1/spark-2.3.1-bin-hadoop2.7.tgz" \
&& tar xzf spark-2.3.1-bin-hadoop2.7.tgz \
&& rm spark-2.3.1-bin-hadoop2.7.tgz \
&& mv spark-2.3.1-bin-hadoop2.7 spark

ENV SPARK_HOME /usr/spark

RUN mkdir -p /usr/spark/work/ \
&& chmod -R 777 /usr/spark/work/

ENV SPARK_MASTER_PORT 7077

ENV PATH=$PATH:$SPARK_HOME/bin/

CMD /usr/spark/bin/spark-class org.apache.spark.deploy.master.Master


##########
RUN pip install --upgrade pip
RUN pip install numpy scipy
RUN pip install -U scikit-learn

# Set up the program in the image

ENV PATH="/opt/program:${PATH}"

COPY program /opt/program
WORKDIR /opt/program

