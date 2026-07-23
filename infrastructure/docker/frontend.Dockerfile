# =============================================================================
# Stage 1: Build
# =============================================================================
FROM node:20-alpine AS builder

ARG API_URL=http://localhost:9000
ARG VITE_API_BASE_URL=http://localhost:9000
ARG ENVIRONMENT=development

ENV VITE_API_URL=$API_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_ENVIRONMENT=$ENVIRONMENT
ENV NODE_ENV=production

WORKDIR /app

RUN chown -R node:node /app && \
    apk add --no-cache python3 make g++

USER node

COPY apps/web/package.json apps/web/package-lock.json* apps/web/ ./
RUN npm ci --no-audit --no-fund

COPY apps/web/ .

RUN npm run build

# =============================================================================
# Stage 2: Serve
# =============================================================================
FROM nginx:1.27-alpine

ARG ENVIRONMENT=development
ENV ENVIRONMENT=$ENVIRONMENT

RUN rm -f /etc/nginx/conf.d/default.conf && \
    rm -rf /var/cache/nginx && \
    addgroup -S appgroup && \
    adduser -S -G appgroup -s /sbin/nologin nginx

COPY --from=builder /app/dist /usr/share/nginx/html
COPY infrastructure/docker/nginx-spa.conf /etc/nginx/conf.d/default.conf

RUN chown -R nginx:appgroup /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:appgroup /var/log/nginx && \
    chown -R nginx:appgroup /etc/nginx && \
    touch /var/run/nginx.pid && \
    chown nginx:appgroup /var/run/nginx.pid

USER nginx

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
