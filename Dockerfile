FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
ENV TZ=Asia/Shanghai
ENV PORT=8080
ENV SUPERUSER=""
ENV TELEGRAM_BOT_TOKEN=""
ENV METUBE_ENDPOINT="http://metube:8081"
ENV SIMPLE_COMMAND="1"
ENV PROGRESS_ENABLED="true"
ENV PROGRESS_INTERVAL_SECONDS="5"
ENV PROGRESS_TIMEOUT_SECONDS="1800"

COPY . /app

RUN chmod +x /app/start.sh

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "httpx>=0.27.0,<1.0.0" \
    "nonebot-plugin-alconna>=0.59.4,<1.0.0" \
    "nonebot2[fastapi,httpx]>=2.4.3,<3.0.0" \
    "nonebot-adapter-telegram>=0.1.0b20" \
    "nonebot-plugin-waiter>=0.8.1"

CMD ["/bin/bash", "/app/start.sh"]
