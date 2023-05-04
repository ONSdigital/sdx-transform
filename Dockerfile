FROM eu.gcr.io/ons-sdx-ci/sdx-gcp:1.1.2
RUN apt-get update && apt-get install -y poppler-utils
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "./run.py"]
