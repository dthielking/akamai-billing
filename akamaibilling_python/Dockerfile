FROM amazonlinux:latest
WORKDIR /app

ADD akamai_billing.py /app
ADD configuration.json /app
ADD requirements.txt /app

RUN yum -y update && yum -y install \
  unzip \
  aws-cli \
  python36 \
  python36-pip

RUN pip-3.6 install -r ./requirements.txt

RUN yum clean all

USER root

CMD [ "-c", "/app/configuration.json" ]
ENTRYPOINT ["python3", "/app/akamai_billing.py"]
