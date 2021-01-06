# googlenews-bot

## Requirements

```bash 
pip install pandas googlenews
```

### Settings

  * `-h`, `--help`            show this help message and exit

  * `-f` DATA_FILENAME, `--data-filename` DATA_FILENAME Filename of the data collected.
			
  * `-l` LANG, `--langage` LANG Language for the news.
			
  * `-p` PERIOD, `--period` PERIOD period of the news research.
			
  * `-k` KEYWORDS, `--keywords` KEYWORDS  Research keywords.
			
  * `-v`, `--verbose`         Display log information on stardard output.
  
  * `-s` SEPARATOR, `--separator` SEPARATOR Add separator for csv file
			
  * `-d`, `--debug`           Display debug on stardard output.
  
  * `--links`               Add the links of the image and of address

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

