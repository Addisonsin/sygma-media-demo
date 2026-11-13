# CMS platform: dashboard + API + Sygma static source for publish copies
FROM node:20-alpine AS ui
WORKDIR /ui
COPY platform/dashboard/package.json platform/dashboard/package-lock.json* ./
RUN npm install
COPY platform/dashboard/ ./
RUN npm run build

FROM python:3.11-slim AS api
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*
COPY platform/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY platform/api/app ./app
COPY --from=ui /ui/dist ./static_ui
COPY web-clones/01-sygma-media /site/sygma-media
COPY platform/schemas/v1 /app/schemas/v1
ENV STATIC_SITE_ROOT=/site/sygma-media
ENV SCHEMA_ROOT=/app/schemas/v1
ENV DATABASE_URL=sqlite:////data/platform.db
ENV MEDIA_LOCAL_ROOT=/data/media
ENV PUBLISH_OUTPUT_ROOT=/data/builds
ENV STATIC_UI_ROOT=/app/static_ui
EXPOSE 8080
VOLUME ["/data"]
CMD ["sh", "-c", "mkdir -p /data/media /data/builds && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
