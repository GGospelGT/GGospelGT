FROM node:20-alpine AS build
WORKDIR /app/frontend
COPY frontend/package*.json ./
COPY frontend/.npmrc ./
RUN npm ci --legacy-peer-deps
COPY frontend ./
RUN npm run build

FROM nginx:alpine
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/frontend/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]