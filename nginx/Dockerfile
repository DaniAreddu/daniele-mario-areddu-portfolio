# syntax=docker/dockerfile:1
# The single public entry point: reverse-proxies "/" to the frontend service
# and "/api" to the backend service. No static content lives in this image.
FROM nginx:1.27-alpine

RUN addgroup -S app && adduser -S app -G app

COPY gateway.conf /etc/nginx/templates/default.conf.template
COPY proxy-common.conf /etc/nginx/proxy-common.conf

RUN sed -i 's,/run/nginx.pid,/tmp/nginx.pid,' /etc/nginx/nginx.conf && \
    touch /tmp/nginx.pid && \
    chown -R app:app /etc/nginx/conf.d /tmp/nginx.pid /var/cache/nginx /etc/nginx/templates

ENV FRONTEND_UPSTREAM=frontend:8080 \
    BACKEND_UPSTREAM=backend:8000 \
    CONTENT_SECURITY_POLICY="default-src 'self'; img-src 'self' data: https://tiles.openfreemap.org; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'; connect-src 'self' https://tiles.openfreemap.org; worker-src 'self' blob:; frame-ancestors 'none'"

USER app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost:8080/healthz >/dev/null || exit 1

CMD ["nginx", "-g", "daemon off;"]
