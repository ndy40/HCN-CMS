FROM python:3.9.5-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /app/
COPY ../Pipfile* /app
RUN pip install pipenv && pipenv install --system
COPY . /app/
EXPOSE 8000
CMD ["/usr/local/bin/pipenv","run", "gunicorn", "backend.wsgi", "-w 4", "-b :8000"]


