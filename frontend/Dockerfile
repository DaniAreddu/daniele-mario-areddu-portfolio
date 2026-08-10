# syntax=docker/dockerfile:1

FROM node:20-slim AS base
WORKDIR /app

# ---------------------------------------------------------------------------
# deps: install dependencies only, cached separately from application source
# ---------------------------------------------------------------------------
FROM base AS deps
COPY package.json package-lock.json ./
RUN npm ci

# ---------------------------------------------------------------------------
# development: full node_modules, source bind-mounted, Vite dev server
# ---------------------------------------------------------------------------
FROM deps AS development
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ---------------------------------------------------------------------------
# build: production bundle
# ---------------------------------------------------------------------------
FROM deps AS build
COPY . .
ARG VITE_API_BASE_URL=/api/v1
ARG VITE_MAP_STYLE_URL=https://tiles.openfreemap.org/styles/liberty
ARG VITE_SITE_URL=
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL \
    VITE_MAP_STYLE_URL=$VITE_MAP_STYLE_URL \
    VITE_SITE_URL=$VITE_SITE_URL
RUN npm run build

# ---------------------------------------------------------------------------
# production: static assets only, served by the shared Nginx gateway image
# ---------------------------------------------------------------------------
FROM nginx:1.27-alpine AS production
RUN addgroup -S app && adduser -S app -G app
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx/frontend.conf /etc/nginx/conf.d/default.conf
RUN sed -i 's,/run/nginx.pid,/tmp/nginx.pid,' /etc/nginx/nginx.conf && \
    touch /tmp/nginx.pid && \
    chown -R app:app /usr/share/nginx/html /etc/nginx/conf.d /tmp/nginx.pid /var/cache/nginx
USER app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost:8080/ >/dev/null || exit 1
CMD ["nginx", "-g", "daemon off;"]
