FROM node:16-alpine as build

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend/ /app/frontend/
RUN mkdir -p /app/backend/dist
RUN npm run build

FROM python:3.7-slim as final
WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY --from=build /app/backend/ .

EXPOSE 9797
ENV COUCHDB_URL ''

ENTRYPOINT [ "python", "app.py" ]