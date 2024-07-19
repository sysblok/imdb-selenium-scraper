import csv

from src.models import FestivalScrapingRequest, FestivalMovieData
from src.scraper import IMDBScraper

if __name__ == '__main__':
    scraper = IMDBScraper()
    
    requests = [
        FestivalScrapingRequest(
            'Berlin International Film Festival',
            'https://www.imdb.com/event/ev0000091',
            ['2015'],
            {
                'Golden Berlin Bear': ['Best Film', None]
            }
        ),
        FestivalScrapingRequest(
            'Cannes Film Festival',
            'https://www.imdb.com/event/ev0000147',
            ['2000'],
            {
                'Palme d\'Or': [None]
            }
        ),
    ]

    for request in requests:
        result = scraper.scrape(request)
        if request.years:
            filename = f'data/movies-{request.name}-{",".join(request.years)}.csv'
        else:
            filename = f'data/movies-{request.name}.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            FestivalMovieData.write_header_row(writer)
            for movie_data in result:
                movie_data.write_row(writer)
