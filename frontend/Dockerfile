# Build stage
FROM node:lts-alpine as builder

WORKDIR /app

COPY app/package*.json .

RUN npm install

COPY /app .

RUN chown -R node:node /app

RUN npm run build

# Production stage with Nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]