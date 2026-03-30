FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src/
COPY data/ /app/data/

RUN useradd --create-home --shell /usr/sbin/nologin licican \
    && chown -R licican:licican /app

USER licican

CMD ["python", "-m", "licican.app"]
