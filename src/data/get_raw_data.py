# -*- coding: utf-8 -*-
import os
import logging
import click
import requests
import json
from dotenv import find_dotenv, load_dotenv


def get_auth_headers():
    LICHESS_TOKEN = os.getenv("LICHESS_TOKEN")
    headers = {"Authorization": "Bearer {}".format(LICHESS_TOKEN)}
    headers.update({"Accept": "application/x-ndjson"})

    return headers


def get_username(headers=get_auth_headers()):
    test_url = "https://lichess.org/api/account"
    r = requests.get(test_url, headers=headers)
    username = r.json().get('username')

    return username


def get_data_dump(username=get_username(), headers=get_auth_headers()):
    games_url = "https://lichess.org/api/games/user/{}".format(username)
    r = requests.get(games_url, headers=headers)
    dump = [json.loads(text) for text in r.text.split('\n')[:-1]]

    return dump


@click.command()
@click.argument('output_filepath', type=click.Path())
def main(output_filepath):
    """ Runs data scraping scripts to put raw data into (../raw)
    """
    logger = logging.getLogger(__name__)

    headers = get_auth_headers()
    username = get_username(headers)
    dump = get_data_dump(username, headers)

    logger.info('outputting {} games from {} to {}'.format(len(dump),
                                                           username,
                                                           output_filepath))

    with open(output_filepath, 'w') as outfile:
        json.dump(dump, outfile)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
