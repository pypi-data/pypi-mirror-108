"""TODO docstring"""
from hashlib import sha256
from typing import Union

import click
from click import Context

from seminar.apis import hugo
from seminar.models import Meeting
from seminar.utils import search, j2env, Config
from seminar import pass_config

from seminar.commands import query_args, query_kwargs


@click.group(name="markdown")
@click.option(*query_args, **query_kwargs)
@pass_config
def cli(cfg, query: str = ""):
    r"""Interact with a Meeting’s SummaryFile.

    Specify the name of a :class:`..models.Meeting` to perform operations over the
    SummaryFiles related to said :class:`..models.Meeting`.
    """
    search.for_meeting(cfg, query)
    pass


@cli.command()
@click.pass_context
def make_summaryfile(ctx: Context, mtg: Meeting):
    r"""Creates the default SummaryFile for a Meeting."""
    ext = ctx.obj.settings.suffixes.simplesummary
    path = mtg.as_file(prefix=ctx.obj.path).with_suffix(ext)

    if not path.exists() or path.stat().st_size == 0:
        simple_instructions = j2env.get_template("summaryfile.md.j2")
        with path.open("w") as f:
            f.write(simple_instructions.render(meeting=mtg))


@cli.command()
@click.pass_context
def make_post(ctx: Context, mtg: Meeting, weight=-1):
    r"""Prepares to export the Meeting SummaryFile to the web."""
    ext = ctx.obj.settings.suffixes.simplesummary
    path = mtg.as_file(prefix=ctx.obj.path).with_suffix(ext)

    try:
        with path.open("r", encoding="utf-8") as f:
            md = f.read()
    except FileNotFoundError:
        return False

    if not diff_summaryfile(ctx.obj, mtg):
        return False

    ctx.invoke(hugo.touch_meeting, mtg=mtg, body=md, weight=weight, from_nb=False)

    return True


def diff_summaryfile(cfg: Config, mtg: Meeting) -> None:
    r"""Determines if the Meeting's SummaryFile differs the default one."""
    tmpl = j2env.get_template("summaryfile.md.j2").render(meeting=mtg)

    try:
        ext = cfg.settings.suffixes.simplesummary
        path = mtg.as_file().with_suffix(ext)
        with path.open("r", encoding="utf-8") as f:
            disk = f.read()
    except FileNotFoundError:
        return True

    tmpl_sha = sha256(tmpl.encode("utf-8")).hexdigest()
    disk_sha = sha256(disk.encode("utf-8")).hexdigest()

    return tmpl_sha != disk_sha


@cli.command()
@click.pass_context
def cleanup(ctx: Context, mtg: Meeting) -> None:
    r"""Delete empty Markdown files associated with .Meeting."""
    if diff_summaryfile(ctx.obj, mtg):
        ext = ctx.obj.settings.suffixes.simplesummary
        mtg.as_file().with_suffix(ext).unlink(missing_ok=True)
