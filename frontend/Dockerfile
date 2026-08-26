FROM node:24.14.1-slim

WORKDIR /frontend

RUN corepack enable

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

CMD ["pnpm","dev", "--host"]
