FROM python:3.12
WORKDIR /usr/local/app

EXPOSE 5000

# Set up virtual environment
RUN pip install --no-cache-dir scipy flask librosa

# Set up an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["/bin/bash"]

