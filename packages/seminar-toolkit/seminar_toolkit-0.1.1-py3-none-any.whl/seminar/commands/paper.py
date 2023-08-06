""" TODO docstring """
from typing import Union

import requests
import click

from seminar.models import Meeting
from seminar.utils import search, requests_headers
from seminar import pass_config
from seminar.commands import query_args, query_kwargs
from seminar.utils import Config


@click.group(name="paper", help="Strictly interacts with a Meeting's papers.")
@click.option(*query_args, **query_kwargs)
@click.pass_obj
def cli(cfg: Config, query: str = ""):
    r"""Interact with a Meeting’s assocaited readings.

    Specify the name of a :class:`seminar.models.Meeting` to perform operations over the
    readings related to said :class:`seminar.models.Meeting`.
    """
    search.for_meeting(cfg, query)


@cli.command()
@click.pass_obj
def download(cfg: Config, mtg: Meeting):
    """Downloads papers and names them based on keys for meetings."""
    if mtg.papers is None:
        return

    folder = cfg.path / mtg.path

    for title, link in mtg.papers.items():
        try:
            with (folder / f"{title}.pdf").open("wb") as pdf:
                pdf.write(requests.get(link, headers=requests_headers).content)
            # TODO Check for corruptness / PDF headers
        except ConnectionError:
            raise ConnectionError(
                f"Failed to connect to {link}, please check it produces a PDF."
            )
