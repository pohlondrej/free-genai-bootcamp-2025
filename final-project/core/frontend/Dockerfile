# Build stage
FROM node:18

WORKDIR /app

COPY app/package*.json ./
RUN npm install

COPY app/ .

EXPOSE 4200

# Install Angular CLI globally
RUN npm install -g @angular/cli

CMD ["ng", "serve", "--host", "0.0.0.0"]