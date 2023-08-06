"""TODO docstring"""
import re

import click
from click import Context

from seminar import pass_config
from seminar.utils import search
from seminar.commands import query_args, query_kwargs


@click.group(name="meeting")
@click.option(*query_args, **query_kwargs)
@click.pass_context
def cli(ctx, query: str = ""):
    r"""Runs the Meeting pipeline for whichever meeting(s) is(are) requested."""
    search.for_meeting(ctx.obj, query)
    pass


@cli.command()
@click.pass_context
def touch(ctx: Context):
    r"""Mimics Unix `touch` and creates/updates Meetings.

    Generates and standardizes Solutionbooks, SummaryFiles, and auxiliary
    :py:class:`Meeting` contents.
    """
    from seminar.commands import notebook, markdown, paper

    for meeting in ctx.obj.meetings:
        # ctx.params["query"] = meeting

        # Primary Meeting contents, strictly one of these should be filled
        ctx.invoke(notebook.make_solutionbook, mtg=meeting)
        ctx.invoke(markdown.make_summaryfile, mtg=meeting)

        # Auxiliary Meeting contents, none of these must to be used
        ctx.invoke(notebook.kaggle_metadata, mtg=meeting)
        ctx.invoke(paper.download, mtg=meeting)


@cli.command()
@click.pass_context
def publish(ctx: Context):
    r"""Prepares "camera-ready" versions of Meetings for public consumption.

    Compiles a [semi-]completed Solutionbook or SummaryFile into formats ready for
    publication on the web and other useful platforms. (e.g. if using Solutionbooks,
    an advantageous publication venue is Kaggle.)

    """
    from seminar.commands import notebook, markdown
    from seminar.apis import hugo

    start = -1 if len(ctx.obj.meetings) < len(ctx.obj.syllabus) else 0

    for weight, meeting in enumerate(ctx.obj.meetings, start=start):
        if re.match("meeting\d\d", meeting.filename):
            # TODO provide failure message
            continue

        ctx.invoke(notebook.make_workbook, mtg=meeting)
        ctx.invoke(notebook.push_kaggle, mtg=meeting)

        export_nb = ctx.invoke(notebook.make_post, mtg=meeting, weight=weight)
        export_md = ctx.invoke(markdown.make_post, mtg=meeting, weight=weight)

        # TODO check XOR(export_nb, export_md)
        try:
            if bool(export_nb) == bool(export_md):
                # TODO write blank to disk
                ctx.invoke(
                    hugo.touch_meeting,
                    mtg=meeting,
                    body="",
                    weight=weight,
                    from_nb=False,
                )
                raise ValueError(
                    "Use of Solutionbook OR Markdown is mutually exclusive. Writing only meeting metadata."
                )
        except ValueError as e:
            print(str(e))
