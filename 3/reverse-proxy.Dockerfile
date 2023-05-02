# Use nginx as the base image
FROM nginx
# Override default configuration with reverse proxy configuration
COPY ./reverse-proxy.conf /etc/nginx/conf.d/default.conf
