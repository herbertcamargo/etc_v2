## Build stage
FROM node:16-alpine as build

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install

# Copy source code
COPY . .

# Expose development port
EXPOSE 3000

# Create production build (for production stage)
RUN npm run build

## Production stage
FROM nginx:alpine as production

# Copy build files from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 