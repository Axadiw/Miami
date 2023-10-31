FROM node:18-alpine

RUN apk add --no-cache libc6-compat

COPY . /app
WORKDIR /app
RUN corepack enable
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile --network-timeout 500000; \
  else echo "Lockfile not found." && exit 1; \
  fi

RUN yarn build
ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

RUN chown nextjs:nodejs .next

COPY --chown=nextjs:nodejs /app/.next/standalone ./
COPY --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
