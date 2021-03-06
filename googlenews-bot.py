# Important import
import os
import sys
from GoogleNews import GoogleNews
import time
import pandas as pd
import argparse
import notify2
import pylog
import pkg_resources

logs = pylog.adv_color_log('Googlenews-bot')
notify2.init('Googlenews-bot')
n = notify2.Notification("Googlenews-bot",
                         "News has been added",
                         "info"   # Icon name
                        )
no_data = notify2.Notification("Googlenews-bot",
                         "No news data added",
                         "info"   # Icon name
                        )
no_internet_connected = notify2.Notification("Googlenews-bot",
                         "Unable to retrieve data from news.google.com",
                         "error"   # Icon name
                        )

installed_pkg = {pkg.key for pkg in pkg_resources.working_set}
if 'ipdb' in installed_pkg:
    import ipdb  # noqa: F401

def arg_parser_arguments():
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
    APP_ARG_PARSER.add_argument(
        '--notify',
        dest='notify_mode',
        action='store_true',
        default=False,
        help='Display debug on stardard output.')
    app_config.update(vars(APP_ARG_PARSER.parse_args()))
    return app_config
def googlenews_recovery(app_config):
    googlenews = GoogleNews()
    googlenews.set_lang(app_config["lang"])
    googlenews.set_period(app_config["period"])
    googlenews.get_news(app_config["keywords"])
    return googlenews
app_config = arg_parser_arguments()
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

# Configure research

if app_config['verbose_mode']:
    logs.info('Data retreiving in progress')

googlenews = googlenews_recovery(app_config)
if len(googlenews.results()) <= 0:
    logs.error('Unable to retrieve data from news.google.com')
    if app_config["notify_mode"]:
        no_internet_connected.show()
    sys.exit(0)
    sys.exit(0)
if app_config['verbose_mode']:
    logs.valid('Data retreiving done')

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
if len(googlenews.results()) <= 0:
    logs.error('Unable to retrieve data from news.google.com')
    sys.exit(0)
if len(data_new_df) == 0:
    logs.warning("No new data collected")
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
logs.info(f"Number of data in file: {data_in_file}")
if nb_data_added <= 0:
    logs.warning(f"No new data collected. ")
    if app_config["notify_mode"]:
        no_data.show()
    sys.exit(0)
else:
    logs.info(f"Number of new data added: {nb_data_added}")
    if app_config["notify_mode"]:
        n.show()
    # Save file to disk
    data_df.to_csv(app_config["data_filename"],
                   sep=app_config["separator"],
                   index=False)


sys.exit(0)
