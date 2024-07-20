FROM centos/python-36-centos7
RUN yum update -y && \
    yum install -y gcc openssl-devel bzip2-devel libffi-devel
COPY . /app
WORKDIR /app
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.6 get-pip.py && \
    pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org --timeout 60 -r requirements.txt
ENV PORT 5000
EXPOSE 5000
ENTRYPOINT [ "python"]
CMD [ "app.py"]
