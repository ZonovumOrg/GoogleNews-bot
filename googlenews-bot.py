# Important import
import os
import sys
from GoogleNews import GoogleNews
import time
import pandas as pd
import argparse

import logging
import pkg_resources

installed_pkg = {pkg.key for pkg in pkg_resources.working_set}
if 'ipdb' in installed_pkg:
    import ipdb  # noqa: F401


app_config = {}
app_config["app_name_short"] = "googlenews-bot"
app_config["app_name_long"] = app_config["app_name_short"]
app_config["version"] = "0.0.1"

# CLI parameters management
# -------------------------
APP_ARG_PARSER = argparse.ArgumentParser(
    description=app_config["app_name_short"] + " " + app_config["version"])

APP_ARG_PARSER.add_argument(
    '-f', '--data-filename',
    dest='data_filename',
    action='store',
    default="news.csv",
    help='Filename of the data collected.')

APP_ARG_PARSER.add_argument(
    '-l', '--langage',
    dest='lang',
    action='store',
    default="en",
    help='Language for the news.')

APP_ARG_PARSER.add_argument(
    '-p', '--period',
    dest='period',
    action='store',
    default="7d",
    help='Period of the news research.')

APP_ARG_PARSER.add_argument(
    '--desc',
    dest='add_desc',
    action='store_true',
    default=False,
    help='Add news description to data.')


APP_ARG_PARSER.add_argument(
    '--links',
    dest='add_links',
    action='store_true',
    default=False,
    help='Add the links of both news image and address.')

APP_ARG_PARSER.add_argument(
    '--media',
    dest='add_media',
    action='store_true',
    default=False,
    help='Add media in news data.')

APP_ARG_PARSER.add_argument(
    '--date-string',
    dest='add_date_string',
    action='store_true',
    default=False,
    help='Add date string new publishing info.')

APP_ARG_PARSER.add_argument(
    '-k', '--keywords',
    dest='keywords',
    action='store',
    default="",
    help='Research keywords.')

APP_ARG_PARSER.add_argument(
    '-s', '--separator',
    dest='separator',
    action='store',
    default=";",
    help='Add separator for csv file')

APP_ARG_PARSER.add_argument(
    '--reset-data',
    dest='reset_data',
    action='store_true',
    default=False,
    help='Erase existing data if exists')


APP_ARG_PARSER.add_argument(
    '-v', '--verbose',
    dest='verbose_mode',
    action='store_true',
    default=False,
    help='Display log information on stardard output.')

APP_ARG_PARSER.add_argument(
    '-d', '--debug',
    dest='debug_mode',
    action='store_true',
    default=False,
    help='Display debug on stardard output.')

app_config.update(vars(APP_ARG_PARSER.parse_args()))

# Logging configuration
if app_config["verbose_mode"]:
    logging.basicConfig(stream=sys.stdout,
                        level=logging.INFO)
if app_config["debug_mode"]:
    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG)


# Open news data stored if exists
if os.path.exists(app_config["data_filename"]) and \
   not(app_config["reset_data"]):
    # Load already stored data
    data_df = pd.read_csv(app_config["data_filename"],
                          parse_dates=["datetime"],
                          sep=app_config['separator'])
else:
    # Create new dataframe
    data_df = pd.DataFrame()

# Init Google News handler
googlenews = GoogleNews()

# Configure research
# Use debug logginh for this kind of information
logging.debug('Data retreiving in progress')
googlenews.set_lang(app_config["lang"])
googlenews.set_period(app_config["period"])
googlenews.get_news(app_config["keywords"])
logging.debug('Data retreiving done')

var_index = ['datetime',
             'site',
             'title']

# Select optional data
var_to_keep = []
if app_config['add_links']:
    var_to_keep.extend(["link", "img"])

if app_config['add_media']:
    var_to_keep.append("media")

if app_config['add_date_string']:
    var_to_keep.append("date")

if app_config['add_desc']:
    var_to_keep.append("desc")


# Get new data and transform it into a dataframe
data_new_df = pd.DataFrame(googlenews.results())

if len(data_new_df) == 0:
    logging.info("No new data collected")
    sys.exit(0)
else:
    data_new_df = data_new_df[var_index + var_to_keep]


nb_data_ori = len(data_df)

# Concatenate new data with stored data
data_df = pd.concat([data_df, data_new_df],
                    axis=0)

# data variables
data_df.drop_duplicates(subset=var_index,
                        keep="first",
                        inplace=True)


nb_data_added = len(data_df) - nb_data_ori
data_in_file = len(data_df) + nb_data_ori

# Data information
logging.info(f"Number of data in file: {data_in_file}")
if nb_data_added <= 0:
    logging.info(f"No new data collected. ")
    sys.exit(0)
else:
    logging.info(f"Number of new data added: {nb_data_added}")

    # Save file to disk
    data_df.to_csv(app_config["data_filename"],
                   sep=app_config["separator"],
                   index=False)


sys.exit(0)
