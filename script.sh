docker build -t scraper . && docker run -it --rm --name scraper -v ${PWD}/.downloads:/usr/src/app/.downloads scraper