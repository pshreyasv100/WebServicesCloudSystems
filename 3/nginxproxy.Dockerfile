# Use nginx as the base image
FROM nginx
COPY ./nginxproxy.conf /etc/nginx/conf.d/default.conf
