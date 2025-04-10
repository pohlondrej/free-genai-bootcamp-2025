# Build stage
FROM node:20-slim AS builder

WORKDIR /app
COPY package.json .
RUN npm install

COPY . .
RUN npm run build

# Nginx stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist/example-plugin/* /usr/share/nginx/html/

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 4201
CMD ["nginx", "-g", "daemon off;"]
