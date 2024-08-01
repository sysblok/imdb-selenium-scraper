from tqdm import tqdm
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from src.models import FestivalScrapingRequest, FestivalMovieData

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

class IMDBScraper:
    def __init__(self) -> None:
        self.options = Options()
        self.options.add_argument('--headless=new')
        self.options.add_argument(f'user-agent={USER_AGENT}')

    def _get_driver(self) -> webdriver.Chrome:
        return webdriver.Chrome(options=self.options)

    def scrape(self, req: FestivalScrapingRequest) -> List[FestivalMovieData]:
        self.driver = self._get_driver()
        try:
            year_urls = self._get_year_urls(req)
        except Exception as e:
            print(f'FATAL cant get years for fest {req.name}: {e}')
        result = []
        for year, year_url in year_urls.items():
            try:
                movies = self._get_movies(req, year, year_url, req.award_categories)
            except Exception as e:
                print(f'FATAL cant get movies for year {year}, url={year_url}: {e}')
                continue
            print(f'{req.award_categories} for {year} got {len(movies)} movies: {year_url}', flush=True)

            # get movies data
            for movie in tqdm(movies):
                result.append(self._get_movie_data(movie))

        return result
    
    def _get_year_urls(self, req: FestivalScrapingRequest):
        self._get_page_with_cache(self.driver, req.url)
        year_row_blocks = self.driver.find_elements(By.CLASS_NAME, 'event-history-widget__years-row')
        # key: year, value: url
        urls = {}
        for year_row_block in year_row_blocks:
            for b in year_row_block.find_elements(By.TAG_NAME, 'a'):
                year = b.text
                if year == '2024' or (req.years and year not in req.years):
                    # 2024s are often incomplete
                    continue
                urls[year] = b.get_attribute('href').replace('file://', 'https://www.imdb.com')
        return urls
    
    def _get_movies(self, req: FestivalScrapingRequest, year: str, year_url: str, award_categories: Dict[str, List[Optional[str]]]) -> List[FestivalMovieData]:
        self._get_page_with_cache(self.driver, year_url)
        award_blocks = self.driver.find_elements(By.CLASS_NAME, 'event-widgets__award')
        result = []
        for award_block in award_blocks:
            # filter through awards
            award_name = award_block.find_element(By.CLASS_NAME, 'event-widgets__award-name').text
            if award_name not in award_categories.keys():
                continue
            award_category_blocks = award_block.find_elements(By.CLASS_NAME, 'event-widgets__award-category')
            # get blocks containing categories, None means no category
            # for example: https://www.imdb.com/event/ev0000681/1949/1/
            category_blocks = {}
            for b in award_category_blocks:
                try:
                    award_category_name = b.find_element(By.CLASS_NAME, 'event-widgets__award-category-name').text
                except:
                    award_category_name = None
                if award_category_name in award_categories[award_name]:
                    category_blocks[award_category_name] = b
            for award_category_name, block in category_blocks.items():
                movie_blocks = block.find_elements(By.CLASS_NAME, 'event-widgets__award-nomination')
                for movie_block in movie_blocks:
                    # extract info about winner
                    try:
                        movie_block.find_element(By.CLASS_NAME, 'event-widgets__winner-badge')
                        winner = True
                    except:
                        winner = False
                    nominees_block = movie_block.find_element(By.CLASS_NAME, 'event-widgets__primary-nominees')
                    movie_url = nominees_block.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('file://', 'https://www.imdb.com')
                    movie_data = FestivalMovieData(
                        req.name,
                        year,
                        award_name,
                        movie_url,
                        winner,
                        award_category_name,
                    )
                    result.append(movie_data)
        return result
    
    def _get_movie_data(self, movie: FestivalMovieData) -> FestivalMovieData:
        self._get_page_with_cache(self.driver, movie.url)

        try:
            title = self.driver.find_element(By.CLASS_NAME, 'hero__primary-text').text
        except:
            title = None
        try:
            length = self.driver.find_element(By.XPATH, '//li[@data-testid="title-techspec_runtime"]/div').text
        except:
            length = None

        try:
            credits_blocks = self.driver.find_elements(By.XPATH, '//li[@data-testid="title-pc-principal-credit"]')
            directors = []
            for block in credits_blocks:
                if 'Director' in block.text:
                    directors = [b.text for b in block.find_elements(By.CLASS_NAME, 'ipc-metadata-list-item__list-content-item')]
        except:
            directors = []

        try:
            country_blocks = self.driver.find_elements(By.XPATH, '//a[contains(@href, "country_of_origin")]')
            countries = [block.text for block in country_blocks]
        except:
            countries = []

        movie.fill_data(
            title,
            length,
            directors,
            countries,
        )
        return movie

    def _get_page_with_cache(self, driver: webdriver.Chrome, url: str, cache_enabled=True) -> None:
        # filename = f'pages/{url.replace("/", "-").replace("?", "-")}.html'
        # if os.path.exists(filename):# and cache_enabled:
        #     driver.get(f'file://{os.getcwd()}/{filename}')
        #     return
        driver.get(url)
        # html = driver.page_source
        # with open(filename, 'w', encoding='utf-8') as f:
        #     f.write(html)

