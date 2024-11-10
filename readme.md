# Kopia strony Yarnstreet.com

# Kroki instalacyjne
1. Sklonuj repozytorium.
2. Skopiuj *docker-compose.override.yml.example* bez końcowego '.example' i zmień wartości w środku zgodnie ze swoim środowiskiem.
3. Użyj komendy `docker-compose up` w środku folderu 'build'.
4. Użyj następujących komend:
```
docker exec -it nadruk-prestashop chown -R www-data:www-data /var/www/html/
docker exec -it nadruk-prestashop chmod -R 755 /var/www/html/
```
5. Środowisko powinno być gotowe.
