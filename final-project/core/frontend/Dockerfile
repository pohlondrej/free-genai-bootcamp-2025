# Build stage
FROM node:20-slim

ARG APP_DIR
ARG MODULES_DIR

WORKDIR /app

COPY $APP_DIR/package*.json ./
RUN npm install

COPY $APP_DIR/ .
COPY $MODULES_DIR/ ./src/app/

EXPOSE 4200

# Install Angular CLI globally
RUN npm install -g @angular/cli

CMD ["ng", "serve", "--host", "0.0.0.0"]