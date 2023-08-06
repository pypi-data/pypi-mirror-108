"""Commands that perform operations over groups (analogous to courses).

Some commands strictly operate over the ``group.yml`` or ``syllabus.yml`` files,
while others enact individual commands over each meeting (analogous to a course
meeting date) item.

.. note:: Be sure to take a look at the general syntax of :ref:`seminar` to ensure you're
          able to interact with the appropriate groups/courses.

"""
import re
import shutil
from pathlib import Path

import click
from click import Context
import pandas as pd

from seminar import models
from seminar.utils import Config


@click.group(name="group")
@click.pass_context
def cli(ctx: Context):
    r"""Performs administrative tasks for a given semester in the Group."""
    pass


@cli.command()
@click.pass_obj
def validate(cfg: Config) -> None:
    r"""Validates the Group's Syllabus is typed properly, sorted, etc."""
    ondisk = list(filter(Path.is_dir, cfg.path.iterdir()))
    empty = len(ondisk) == 0

    group = cfg.group

    g_timedelta = pd.Timedelta(str(group.startdate.time()))
    g_date = group.startdate
    g_weekdelta = pd.Timedelta(7)

    prev_date = g_date
    for idx, meeting in enumerate(cfg.syllabus):
        if re.search(r"meeting\d\d", meeting.filename):
            continue
        if empty or meeting.room == "":
            meeting.room = ctx.obj.group.room
        if g_date.time().hour != 0 and meeting.date.time().hour == 0:
            meeting.date += g_timedelta
        if (meeting.date - prev_date) % g_weekdelta != pd.Timedelta(0):
            print(
                "Not a N-weekly gap. "
                f"The current gap for {meeting} is {(meeting.date - prev_date)}. "
                "Not a failure condition, but take note."
            )
        prev_date = meeting.date

    g_authors = set(map(str.lower, cfg.group.authors))
    for meeting in cfg.syllabus:
        if re.search(r"meeting\d\d", meeting.filename):
            continue
        m_authors = set(map(str.lower, meeting.authors))
        # TODO check how the authors are missing
        if not m_authors and meeting.title and meeting.filename:
            _msg = f"Meeting {meeting} has no authors."
        elif not m_authors.intersection(g_authors):
            _msg = f"Meeting {meeting} authors not in Group {ctx.obj.group} authors."
        else:
            continue
        print(_msg)

    try:
        n_mtgs = len(cfg.syllabus)
        n_uniq = len({m.date for m in cfg.syllabus})
        assert n_mtgs == n_uniq
    except AssertionError:
        pass

    ctx.obj.syllabus = sorted(cfg.syllabus, key=lambda m: m.date)

    # region Write out validated syllabus
    syllabus_yml = cfg.path / "syllabus.yml"
    models.to_yaml(cfg.syllabus, syllabus_yml)
    # endregion


@cli.command()
@click.pass_obj
def touch(cfg: Config):
    r"""Mimics Unix `touch` and creates/updates the Group."""
    from seminar.apis import hugo

    # region Make this semester's meeting directories
    # In the repository
    cfg.path.mkdir(exist_ok=True)
    # On the website
    hugo.touch_semester(ctx)
    # endregion

    # region Write to `group.yml`
    group_yml = cfg.path / "group.yml"
    models.to_yaml(cfg.group, group_yml)
    # endregion

    # region Write to `syllabus.yml`
    syllabus_yml = cfg.path / "syllabus.yml"
    models.to_yaml(cfg.syllabus, syllabus_yml)
    # endregion

    # region Create and/or rename the Meeting directories
    # NOTE this section strictly creates directories and renames. If you want to create
    #  actual meeting files, use `meeting.touch`.
    def getid(p):
        return str((p / ".metadata").open("r", encoding="utf-8").read())

    syllid = {str(m.id): cfg.path / str(m) for m in cfg.syllabus}
    ondisk = sorted(list(filter(Path.is_dir, cfg.path.glob("??-??-*/"))))
    ondisk = {getid(p): p for p in ondisk}

    for id, meeting in syllid.items():
        try:
            ondisk[id].rename(meeting)
        except (KeyError, FileNotFoundError):
            meeting.mkdir()
            (meeting / ".metadata").open("w", encoding="utf-8").write(str(id))
            ondisk[id] = meeting

        prv = ondisk[id].stem[6:]  # only consider filenames
        needs_rename = filter(lambda x: x.stem.startswith(prv), meeting.iterdir())

        new = meeting.stem[6:]
        for child in needs_rename:
            ext = "".join(child.suffixes)
            child.rename(child.parent / f"{new}{ext}")
    # endregion

    # region Update Author Profiles on the website
    for author in cfg.group.authors:
        hugo.touch_author(ctx, author.lower())
    # endregion


@cli.command()
@click.pass_context
def new_semester(ctx: Context) -> str:
    r"""Creates a new semester. Filters the {group}.yml context for semester creation. Calls `group.touch` post completion."""
    from seminar.models import Group, Meeting
    from seminar.utils.ucfcal import make_schedule

    cfg = ctx.obj

    assert not isinstance(cfg.group, Group), "Already made a new semester."

    kwargs = {"name": cfg.group, "semester": cfg.semester}
    group = Group(**kwargs)

    calendar = make_schedule(group, new_semester=True)
    syllabus = [
        Meeting(title=f"meeting{idx:02d}", filename=f"meeting{idx:02d}", date=date)
        for idx, date in enumerate(calendar)
    ]

    cfg.group = group
    cfg.semester = group.semester
    if cfg.path.parts.count(cfg.semester) < 1:
        cfg.path /= group.semester
    cfg.syllabus = syllabus

    ctx.invoke(touch)


# @task(pre=[preprocess], post=[status_dump])
# @click.command()
# def publish(ctx):
#     """Prepares "camera-ready" versions of the Group for public consumption."""
#     pass


@cli.command()
@click.pass_context
def cleanup(ctx: Context) -> str:
    r"""Cleans up excess files, roles, and the like for a Group."""
    from seminar.apis import hugo
    from seminar.commands import notebook, markdown

    # region Cleanup lingering syllabus entries and directories
    def isa_template(s: str):
        return re.search(r"meeting\d\d", s)

    ctx.obj.syllabus = list(
        filter(lambda m: not isa_template(m.filename), ctx.obj.syllabus)
    )

    dirs = filter(Path.is_dir, ctx.obj.path.iterdir())
    template_dirs = filter(lambda p: isa_template(p.stem), dirs)
    template_dirs = [shutil.rmtree(str(p)) for p in template_dirs]
    # endregion

    # region Cleanup unused default files (e.g. blank Notebooks, SimpleSummaries, etc.)
    for idx, meeting in enumerate(ctx.obj.syllabus):
        ctx.invoke(markdown.cleanup, meeting)
        ctx.invoke(notebook.cleanup, meeting)
        try:
            items = list(map(str, list(meeting.as_file().parent.iterdir())))
            assert len(items) > 0  # avoid repeating code
        except (AssertionError, FileNotFoundError) as e:
            pass
        finally:
            del ctx.obj.syllabus[idx]
            continue

        try:
            ends_markdown = map(lambda x: x.endswith("md"), items)
            ends_notebook = map(lambda x: x.endswith("ipynb"), items)
            assert any(ends_markdown) or any(ends_notebook)
        except AssertionError:
            shutil.rmtree(str(meeting.as_file().parent))
            del ctx.obj.syllabus[idx]
    # endregion

    ctx.invoke(hugo.cleanup_authors)

    # TODO rewrite cleaned syllabus/group
    ctx.invoke(touch)
