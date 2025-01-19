# Kopia strony Yarnstreet.com

## Użyte technologie

1. [Prestashop](https://pl.prestashop.com/) w wersji 1.7.8 - główny silnik sklepu internetowego.
2. [MySQL](https://www.mysql.com/) w wersji 8.0 - baza danych całego projektu.
3. [Python](https://www.python.org/) w wersji 3.12 z bibliotekami requests oraz BeautifulSoup4 - scraping oryginalnego sklepu oraz połączenie z REST API Prestashop.
4. [Selenium](https://www.selenium.dev/) w wersji 2.26.0 oraz [Java](https://www.java.com/en/) w wersji 23 - testy projektu.
5. [Docker](https://www.docker.com/) - unifikacja środowiska docelowego, ułatwienie konfiguracji, oraz konteneryzacja elementów aplikacji.

## Członkowie zespołu

- Jakub Jędrzejczyk, 188752
- Adrian Dybowski, 193483
- Anastasiia Lieshchova, 191601
- Yuliia Lieshchova, 191527

## Kroki do włączenia lokalnie.

1. Sklonuj repozytorium.
2. Uruchom skrypt `build.sh` w folderze repozytorium.
3. Użyj komendy `docker-compose up` w środku folderu 'build'.
4. Użyj komendy `sudo docker exec nadruk-mariadb /bin/bash -c 'mysql -u "yarn_user" -p"yarn_password" < /var/lib/mysql/dump.sql'`.
5. Połącz się z _localhost:8443_ i sprawdź sklep.
6. Nie zapomnij użyć komendy `sudo docker exec -i nadruk-mariadb mysqldump -u "yarn_user" -p"yarn_password" --databases prestashop --skip-comments --no-tablespaces > [path]/db/dump.sql` po skończeniu pracy nad sklepem.

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
