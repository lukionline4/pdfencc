FROM centos/python-39-centos7@sha256:5c3d2315a0d3e0faed13b9b8bfe441ae3a3e66f1594460a5e8d070b08d2e84c2

# Set user to root to ensure we have the necessary permissions
USER root

# Set up DNS configuration
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Install pip
RUN curl -k https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.9 get-pip.py && \
    pip install --upgrade pip

# Copy application files
COPY . /app

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org --timeout 60 -r requirements.txt

# Set environment variable for the port
ENV PORT 5000

# Expose the port
EXPOSE 5000

# Set the entrypoint and command
ENTRYPOINT ["python3.9"]
CMD ["app.py"]
