"""The entrypoint of the `seminar` library. Handles general configuration and routing.

.. moduleauthor:: John Muchovej <jmuchovej@gmail.com>
"""
import os
from pathlib import Path

import click
from click import Context

from seminar.models import Group, Meeting
from seminar import group, meeting
from seminar.utils import environment
from seminar.utils.config import Config

from seminar.commands import group, meeting, notebook, markdown, paper
from seminar.models.group import infer_current_semester

APP_DIR = Path(click.get_app_dir("seminar-toolkit"))


def _workdir_update(cwd, update) -> Path:
    dirs = list(filter(Path.is_dir, cwd.iterdir()))
    if (cwd / update) in dirs:
        cwd /= update
    return cwd


def _check_or_set_semester(ctx, param, value):
    if value is None or len(value) == 0:
        return infer_current_semester()
    elif len(value) != 4:
        return click.BadParameter("Must be a 4-character representation.")
    elif not (value[:2] in ["sp", "su", "fa"] and value[2:].isdigit()):
        return click.BadParameter("Must match the following format: (sp|su|fa)XX.")
    return value


@click.group(
    invoke_without_command=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
        # "allow_interspersed_args": True,
    },
)
@click.option(
    "-o",
    "--org",
    "organization",
    type=str,
    required=False,
    default="",
    help="Specifying the organization name helps locate the appropriate `config.yml`.",
)
@click.option(
    "-c",
    "--config",
    "config",
    type=Path,
    default=APP_DIR / "config.yml",
    help="The path to your desired `config.yml`.",
)
@click.option(
    "-g",
    "--group",
    "group",
    type=str,
    required=True,
    help="The group you're modifying.",
)
@click.option(
    "-s",
    "--semester",
    "semester",
    callback=_check_or_set_semester,
    type=str,
    required=True,
    default=infer_current_semester(),
    help="The semester you're modifying.",
)
@click.pass_context
@click.version_option()
@click.help_option()
def seminar(
    ctx: Context,
    organization: str,
    config: Path,
    group: str,
    semester: str,
) -> None:
    from ruamel.yaml import YAML

    yaml = YAML()

    ctx.obj = Config(ci=environment.is_ci())

    cwd = Path().absolute()
    if ctx.obj.ci:
        cwd /= semester
    else:
        cwd = _workdir_update(cwd, group)
        cwd = _workdir_update(cwd, semester)

    ctx.obj.path = cwd
    try_specific_app_dir = bool(organization) and APP_DIR.stem in str(config)
    if try_specific_app_dir and organization not in config.name:
        config = APP_DIR / organization / "config.yml"

    ctx.obj.settings = dict(yaml.load(open(config, "r")))

    os.chdir(cwd)

    try:
        group = ctx.obj.path / "group.yml"
        group = yaml.load(group.open("r", encoding="utf-8"))
        group = Group(**dict(group))
    except FileNotFoundError:
        group = ctx.params["group"]
        semester = ctx.params["semester"]
    finally:
        ctx.obj.group = group
        ctx.obj.semester = semester

    try:
        syllabus = ctx.obj.path / "syllabus.yml"
        syllabus = yaml.load(syllabus.open("r", encoding="utf-8"))
        syllabus = list(map(dict, syllabus))
        syllabus = [Meeting(**kwargs) for kwargs in syllabus]
    except FileNotFoundError:
        syllabus = []
    finally:
        ctx.obj.syllabus = syllabus

    if ctx.obj.ci:
        site_src = Path("/")
    else:
        site_src = ctx.obj.path.parent
        if semester in ctx.obj.path.stem:
            site_src = site_src.parent

    site_src /= ctx.obj.settings.web.repo

    ctx.obj.settings.web.src = site_src
    assert site_src.exists(), site_src

    ctx.obj.settings.web.config = site_src / ctx.obj.settings.web.config
    ctx.obj.settings.web.config = yaml.load(
        ctx.obj.settings.web.config.open("r", encoding="utf-8")
    )


seminar.add_command(group.cli)
seminar.add_command(meeting.cli)
seminar.add_command(notebook.cli)
seminar.add_command(markdown.cli)
seminar.add_command(paper.cli)
