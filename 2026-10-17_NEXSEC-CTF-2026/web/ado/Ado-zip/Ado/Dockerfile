FROM node:22-bookworm-slim AS app

WORKDIR /app

ENV CACHE_DIR=/tmp/cache

COPY --chown=node:node package.json package-lock.json ./
COPY --chown=node:node bodyparser-10.1.1 ./bodyparser-10.1.1
RUN npm ci

COPY --chown=node:node . .
RUN mkdir -p storage/uploads storage/reports node_modules/.cache tmp \
    && chown -R node:node storage node_modules/.cache tmp \
    && cp -r storage /app/storage.seed

COPY --chown=node:node flag.txt /app/flag.txt
RUN chmod 400 /app/flag.txt

COPY --chown=root:root docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

USER node
EXPOSE 3333
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["node", "ace", "serve"]

FROM ghcr.io/puppeteer/puppeteer:22.15.0 AS admin-bot

WORKDIR /home/pptruser/app

COPY --chown=pptruser:pptruser bot/package.json bot/package-lock.json ./
RUN npm ci
COPY --chown=pptruser:pptruser bot/bot.js ./bot.js

USER pptruser
CMD ["npm", "start"]
