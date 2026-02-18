# frontend/Dockerfile
# Purpose: Build the React app and serve it using nginx.
# Input: frontend source code
# Output: container serving static site on port 80

# 1) Build step
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build

# 2) Serve step
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]