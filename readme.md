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






## Użyte wtyczki
- Owl Carousel 2, https://owlcarousel2.github.io/OwlCarousel2/ 
    
    Copyright (c) 2014 Owl
    Modified work Copyright 2016-2018 David Deutsch

    Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

    The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
