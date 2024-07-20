FROM centos/python-36-centos7@sha256:ac50754646f0d37616515fb30467d8743fb12954260ec36c9ecb5a94499447e0

# Set user to root to ensure we have the necessary permissions
USER root

# Set up DNS configuration
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Update CA certificates and install essential tools
RUN yum install -y ca-certificates && \
    update-ca-trust force-enable && \
    yum install -y gcc openssl-devel bzip2-devel libffi-devel

# Copy application files
COPY . /app

# Set the working directory
WORKDIR /app

# Install pip
RUN curl -k https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.6 get-pip.py && \
    pip install --upgrade pip

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org --timeout 60 -r requirements.txt

# Set environment variable for the port
ENV PORT 5000

# Expose the port
EXPOSE 5000

# Set the entrypoint and command
ENTRYPOINT ["python"]
CMD ["app.py"]
