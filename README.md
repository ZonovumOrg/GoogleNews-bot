# googlenews-bot

## Requirements

```bash 
pip install pandas googlenews
```

## Usage

To show the help:
```bash 
python googlenews-bot.py -h
```

Get daily news on bitcoin:
```bash 
python googlenews-bot.py -p 1d -k bitcoin
```
The data is stored in file `news.csv`.

Get last french news on COVID and store it in `covid_news.csv`:
```bash 
python googlenews-bot.py -p 1h -l fr -k COVID -f covid_news.csv
```

