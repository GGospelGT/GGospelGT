FROM node:20-alpine AS build
WORKDIR /app/frontend
COPY GGospelGT/frontend/package*.json ./
RUN npm ci
COPY GGospelGT/frontend ./
RUN npm run build

FROM nginx:alpine
COPY GGospelGT/nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/frontend/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]