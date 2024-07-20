FROM python:3.9

# Set user to root to ensure we have the necessary permissions
USER root

# Set up DNS configuration
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Copy application files
COPY . /app

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org --timeout 60 -r requirements.txt

# Set environment variable for the port
ENV PORT 8080

# Expose the port
EXPOSE 8080

# Set the entrypoint and command
ENTRYPOINT ["python"]
CMD ["app.py"]
