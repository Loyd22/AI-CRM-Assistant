# frontend/Dockerfile
# Purpose: Build the React app and serve it using nginx.
# Input: frontend source code
# Output: container serving static site on port 80

# build step
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# serve step
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80