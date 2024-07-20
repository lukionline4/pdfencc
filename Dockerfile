FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
ENV PORT 5000
EXPOSE 5000
ENTRYPOINT [ "python"]
CMD [ "app.py"]
