# GoogleNews bot
## GoogleNews bot is news retrieval software via the GoogleNews API


### Requirement
You need to perform the following commands to run GoogleNews bot:
```bash
pip3 install -r requirement.txt
```
### Use
Use: `python3 googlenews-bot.py # Params`
To use Google News bot you can add the following parameters:
  * `-h`, `--help`            show this help message and exit
  * `-f` DATA_FILENAME, `--data-filename` DATA_FILENAME Filename of the data collected.
  * `-l` LANG, `--langage` LANG Language for the news.
  * `-p` PERIOD, `--period` PERIOD period of the news research.
  * `-k` KEYWORDS, `--keywords` KEYWORDS  Research keywords.
  * `-v`, `--verbose`         Display log information on standard output.
  * `-s` SEPARATOR, `--separator` SEPARATOR Add separator for csv file
  * `-d`, `--debug`           Display debug on standard output.
  * `--desc`                Add news description to data.
  * `--links`               Add the links of both news image and address.
  * `--media`               Add media in news data.
  * `--date-string`         Add date string new publishing info.
  * `--notify`              Add information notification

Example:

```bash
python3 googlenews-bot.py -l en -k covid --links --desc --media --date-string -f covid_en.csv -p 7d 
```

returns all the english news on the covid in a period of 7 days in the covid_en.csv file with the publication date, description and media.

