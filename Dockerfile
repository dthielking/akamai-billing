FROM amazonlinux:latest
WORKDIR /app
ADD akamai_billing.py /app
ADD akamai_config.json /app
ADD requirements.txt /app
RUN yum -y update
RUN yum -y install unzip aws-cli python36 python36-pip htop
RUN pip-3.6 install -r /app/requirements.txt
USER root
CMD ["python3", "/app/akamai_billing.py"]
