FROM node:16-alpine as build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

ENV BACKEND_URL ''

ENTRYPOINT [ "npm", "run", "upload" ]