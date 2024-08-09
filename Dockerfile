FROM python:3.12.1
LABEL authors="Ivan Mihun"

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --without tray,dev

COPY src ./

CMD ["/bin/sh"]