# Use the official Nginx image from Docker Hub as the base image
FROM nginx:latest

# Copy your 'app' directory content into the Nginx web root directory
# The default web root for Nginx is /usr/share/nginx/html/
COPY ./app /usr/share/nginx/html/

# Expose port 80, which is the default port Nginx listens on
EXPOSE 80

# The Nginx base image already has a CMD instruction to start Nginx,
# so we don't need to add another CMD here unless we want to customize it.