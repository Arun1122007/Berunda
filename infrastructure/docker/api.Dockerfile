# =============================================================================
# Stage 1: Dependencies
# =============================================================================
FROM node:20-slim AS deps

WORKDIR /app

RUN useradd -m -u 1001 nodejs && \
    chown -R nodejs:nodejs /app

USER nodejs

COPY apps/api/package.json apps/api/package-lock.json* ./
RUN npm ci --omit=dev --no-audit --no-fund

# =============================================================================
# Stage 2: Runtime
# =============================================================================
FROM node:20-slim

ARG NODE_ENV=production
ARG CATALYST_ENV=production

ENV NODE_ENV=$NODE_ENV
ENV CATALYST_ENV=$CATALYST_ENV

WORKDIR /app

RUN useradd -m -u 1001 nodejs && \
    chown -R nodejs:nodejs /app

USER nodejs

COPY --chown=nodejs:nodejs --from=deps /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs apps/api/ .

EXPOSE 9000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:9000/health',(r)=>{process.exit(r.statusCode===200?0:1)}).on('error',()=>process.exit(1))"

CMD ["node", "index.js"]
