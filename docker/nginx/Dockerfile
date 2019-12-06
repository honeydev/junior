FROM nginx:1.16.1-alpine

EXPOSE 80

RUN rm /etc/nginx/conf.d/default.conf

COPY docker/nginx/nginx.conf /etc/nginx/conf.d
