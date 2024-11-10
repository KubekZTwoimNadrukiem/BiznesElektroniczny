# Yarnstreet.com copy

# Installation steps
1. Copy repository.
2. Use `docker-compose up` inside of the build folder.
3. Use the following commands:
```
docker exec -it nadruk-prestashop chown -R www-data:www-data /var/www/html/
docker exec -it <prestashop_container_name> chmod -R 755 /var/www/html/
```
