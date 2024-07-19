from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class FestivalMovieData:
    festival_name: str
    festival_year: int
    award: str
    url: str
    winner: bool
    award_category: str = None

    def fill_data(
        self,
        title: str,
        length: str,
        directors: List[str],
        countries: List[str],
    ):
        self.title = title
        self.length = length
        self.directors = directors
        self.countries = countries

    @staticmethod
    def write_header_row(writer):
        writer.writerow(
            [
                'Festival',
                'Year',
                'Award',
                'Award Category',
                'Title',
                'Winner',
                'Length',
                'Directors',
                'Countries',
                'URL',
            ]
        )

    def write_row(self, writer):
        if not self.title:
            print(f'ERR {self.url} lacks title', flush=True)
        if not self.length:
            print(f'ERR {self.url} lacks length', flush=True)
        if not self.directors:
            print(f'ERR {self.url} lacks directors', flush=True)
        if not self.countries:
            print(f'ERR {self.url} lacks countries', flush=True)
        writer.writerow(
            [
                self.festival_name,
                self.festival_year,
                self.award,
                self.award_category,
                self.title,
                self.winner,
                self.length,
                ','.join(self.directors),
                ','.join(self.countries),
                self.url,
            ]
        )

@dataclass
class FestivalScrapingRequest:
    name: str
    url: str
    years: List[int]
    award_categories: Dict[str, List[Optional[str]]]
