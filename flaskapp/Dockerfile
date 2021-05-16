FROM node:16-alpine as build

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend/ /app/frontend/
COPY backend/ /app/backend/
RUN npm run build

FROM python:3.7-slim as final
WORKDIR /app
COPY --from=build /app/backend/ .
RUN pip install -r requirements.txt
EXPOSE 9797
ENV COUCHDB_URL ''

ENTRYPOINT [ "python", "app.py" ]