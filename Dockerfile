FROM python:3.8-slim
RUN apt-get update && apt-get install -y poppler-utils
COPY . /app
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE 5000
CMD ["python", "./run.py"]