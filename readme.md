# Kopia strony Yarnstreet.com

## Użyte technologie

1. [Prestashop](https://pl.prestashop.com/) w wersji 1.7.8 - główny silnik sklepu internetowego.
2. [MySQL](https://www.mysql.com/) w wersji 8.0 - baza danych całego projektu.
3. [Python](https://www.python.org/) w wersji 3.12 z bibliotekami requests oraz BeautifulSoup4 - scraping oryginalnego sklepu oraz połączenie z REST API Prestashop.
4. [Selenium](https://www.selenium.dev/) oraz [Java](https://www.java.com/en/) - testy projektu.
5. [Docker](https://www.docker.com/) - unifikacja środowiska docelowego, ułatwienie konfiguracji, oraz konteneryzacja elementów aplikacji.

## Członkowie zespołu

- Jakub Jędrzejczyk, 188752
- Adrian Dybowski, 193483
- Anastasiia Lieshchova, 191601
- Yuliia Lieshchova, 191527

## Kroki instalacyjne

1. Sklonuj repozytorium.
2. Skopiuj _docker-compose.override.yml.example_ bez końcowego '.example' i zmień wartości w środku zgodnie ze swoim środowiskiem.
3. Użyj komendy `docker-compose up` w środku folderu 'build'.
4. Połącz się z _localhost:[port]_ i sprawdź sklep.
