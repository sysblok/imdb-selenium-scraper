# imdb-selenium-scraper

## Usage

1) Create a virtual environment: `python -m venv env && source env/bin/activate`
2) Install requirements: `python -m pip install -r requirements.txt`
3) Run `main.py`:
```bash
$ python main.py 
{'Golden Berlin Bear': ['Best Film', None]} for 2015 got 19 movies: https://www.imdb.com/event/ev0000091/2015/1/?ref_=ev_eh
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 19/19 [00:43<00:00,  2.30s/it]
{"Palme d'Or": [None]} for 2000 got 23 movies: https://www.imdb.com/event/ev0000147/2000/1/?ref_=ev_eh
 22%|███████████████████████▋                                                                                     | 5/23 [00:14<00:51,  2.86s/it]
```