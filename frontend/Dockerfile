FROM node:lts-alpine

# Create app directory and set working directory
WORKDIR /app

# Copy package files
COPY app/package*.json .

# Install dependencies
RUN npm install

# Copy application code
COPY /app .

# Set correct permissions
RUN chown -R node:node /app

EXPOSE 3000
# Switch to non-root user
USER node
