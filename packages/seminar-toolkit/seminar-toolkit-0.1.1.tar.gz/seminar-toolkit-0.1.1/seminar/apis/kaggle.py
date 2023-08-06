import json
import os
import subprocess
from hashlib import sha256
from typing import Tuple
from pathlib import Path
from tempfile import TemporaryDirectory
import functools

import click
import requests
from click import Context

from seminar.utils import j2env, Config
from seminar.models import Meeting


shell = functools.partial(subprocess.call, shell=True, stdout=subprocess.DEVNULL)


@click.group(name="kaggle")
@click.pass_context
def cli(ctx: Context):
    r"""

    Parameters
    ----------
    ctx: :py:class:`click.Context`
        Click's built-in Context object. This is automatically passed by CLI execution.
    """
    tmp = ctx.obj.kaggle_dir = TemporaryDirectory()

    os.environ["KAGGLE_CONFIG_DIR"] = str(tmp.name)

    with (tmp / "kaggle.json").open("w", encoding="utf-8") as kaggle:
        config = json.loads(os.environ["KAGGLE_CONFIG"])
        json.dump(config, kaggle)

    os.chmod(tmp / "kaggle.json", "600")


@cli.command()
@click.pass_context
def kernel_metadata(ctx: Context, mtg: Meeting):
    r"""Generates `kernel-metadata.json` for each Kaggle competition.

    More info on the Kaggle API `kernel-metadata.json` file:
        https://github.com/Kaggle/kaggle-api/wiki/Kernel-Metadata

    Parameters
    ----------
    ctx: :py:class:`click.Context`
        Click's built-in Context object. This is automatically passed by :py:func:`ctx.invoke`.
    mtg: :py:class:`seminar.models.Meeting`
        The :py:class:`Meeting` to generate the Kaggle Kernel slug.
    """
    if "kaggle" not in mtg or mtg.kaggle is None:
        # TODO check for non-empty notebook
        return

    _username = ctx.obj.settings.kaggle.username

    metadata_j2 = j2env.get_template("kaggle/kernel-metadata.json.j2")

    if type(mtg.kaggle) == bool:
        mtg.kaggle = {}

    use_competitions = mtg.kaggle.get("competitions", False)

    mtg.kaggle["competitions"] = mtg.kaggle.get("competitions", [])
    mtg.kaggle["datasets"] = mtg.kaggle.get("datasets", [])
    mtg.kaggle["kernels"] = mtg.kaggle.get("kernels", [])
    mtg.kaggle["enable_gpu"] = mtg.kaggle.get("enable_gpu", False)

    if use_competitions:
        mtg.kaggle["competitions"].append(slug_competition(ctx.obj, mtg))

    kernel = mtg.as_file().with_name("kernel-metadata.json")
    with kernel.open("w", encoding="utf-8") as f:
        kwargs = {
            "username": _username,
            "slug": slug_kernel(ctx.obj, mtg),
            "kaggle": mtg.kaggle,
            "notebook": mtg.filename,
        }
        json.dump(json.loads(metadata_j2.render(**kwargs)), f, indent=2)


def _pull_kernel(ctx: Context, mtg: Meeting):
    r"""Pull Kaggle Kernel in `kernel-metadata.json` to be diff'd.

    Parameters
    ----------
    ctx: :py:class:`click.Context`
        Click's built-in Context object. This is automatically passed by :py:func:`ctx.invoke`.
    mtg: :py:class:`seminar.models.Meeting`
        The :py:class:`Meeting` to generate the Kaggle Kernel slug.
    """
    _username = ctx.obj.settings.kaggle.username

    existence_test = requests.get(
        f"https://kaggle.com/{_username}/{slug_kernel(ctx.obj, mtg)}"
    )

    if existence_test.status_code != requests.codes.OK:
        return None
    else:
        kaggle_cmd = "kaggle k pull -p /tmp/"
        shell(f"{kaggle_cmd} {_username}/{slug_kernel(ctx.obj, mtg)}")
        return Path("/tmp") / f"{slug_kernel(ctx.obj, mtg)}{mtg.workbook}"


def _diff_kernel(ctx: Context, mtg: Meeting, remote: Path) -> bool:
    r"""Uses `sha256` on local Workbook and Kaggle Kernel to determine if they differ.

    Parameters
    ----------
    ctx: :py:class:`click.Context`
        Click's built-in Context object. This is automatically passed by :py:func:`ctx.invoke`.
    mtg: :py:class:`seminar.models.Meeting`
        The :py:class:`Meeting` know which notebook to source when diff'ing notebooks.
    remote: :py:class:`pathlib.Path`
        The notebook currently hosted on Kaggle Kernels.

    Returns
    -------
    hash_equality: bool
        Returns ``True`` if the local and remote Workbooks differ.
    """
    local = ctx.obj.path / mtg.workbook

    remote_hash = sha256(open(remote, "rb").read()).hexdigest()
    local_hash = sha256(open(local, "rb").read()).hexdigest()

    return remote_hash != local_hash


@cli.command()
@click.pass_obj
def push_kernel(ctx: Context, mtg: Meeting):
    r"""Pushes a Meeting's local Workbook to Kaggle Kernels.

    Parameters
    ----------
    ctx: :py:class:`click.Context`
        Click's built-in Context object. This is automatically passed by :py:func:`ctx.invoke`.
    mtg: :py:class:`seminar.models.Meeting`
        The :py:class:`Meeting` to generate the Kaggle Kernel slug.
    """
    path = _pull_kernel(ctx, mtg)
    diff = _diff_kernel(ctx, mtg, path) if path else True

    if diff:
        cwd = Path().absolute()
        os.chdir(mtg.as_dir())
        shell("kaggle k push")
        os.chdir(cwd)
    else:
        raise ValueError("Kernels are the same")


@cli.command()
@click.pass_context
def create_competition(ctx: Context, mtg: Meeting) -> bool:
    r"""TODO: Create a Meeting's associated Kaggle InClass Competition.

    Parameters
    ----------
    ctx: :py:class:`click.Context`
        Click's built-in Context object. This is automatically passed by :py:func:`ctx.invoke`.
    mtg: :py:class:`seminar.models.Meeting`
        The :py:class:`Meeting` to generate the Kaggle Kernel slug.
    """
    # NOTE this might be doable using https://github.com/puppeteer/puppeteer,
    #   Selenium will definitely work, though
    raise NotImplementedError()


@cli.command()
@click.pass_context
def accept_competition(ctx: Context, mtg: Meeting) -> bool:
    r"""TODO: Accept a Meeting's associated Kaggle InClass Competition rules.

    Parameters
    ----------
    ctx: :py:class:`click.Context`
        Click's built-in Context object. This is automatically passed by :py:func:`ctx.invoke`.
    mtg: :py:class:`seminar.models.Meeting`
        The :py:class:`Meeting` to generate the Kaggle Kernel slug.
    """
    # NOTE this might be doable using https://github.com/puppeteer/puppeteer,
    #   Selenium will definitely work, though
    raise NotImplementedError()


def slug_kernel(cfg: Config, mtg: Meeting) -> str:
    r"""Generates Kaggle Kernel slugs of the form: `<group>-<semester>-<filename>`.
    e.g. If we consider the Spring 2020 "Building AI, the Human Way" lecture, the slug
    would be: `core-fa19-building-ai-the-human-way`.

    Parameters
    ----------
    ctx: :py:class:`click.Context`
        Click's built-in Context object. This is automatically passed by :py:func:`ctx.invoke`.
    mtg: :py:class:`seminar.models.Meeting`
        The :py:class:`Meeting` to generate the Kaggle Kernel slug.

    Return
    ------
    slug: str
        The Kaggle Kernel slug. Viewable at kaggle.com/<kaggle-username>/<slug>
    """
    return f"{cfg.group.name}-{cfg.semester}-{mtg.filename}"


def slug_competition(cfg: Config, mtg: Meeting) -> str:
    r"""Kaggle InClass competitions are listed under general competitions. So, we take
    each meeting's `slug_kernel` and prepend `ORG_NAME` to that – so for AI@UCF, it we
    prepend `ucfai`.

    Parameters
    ----------
    ctx: :py:class:`click.Context`
        Click's built-in Context object. This is automatically passed by :py:func:`ctx.invoke`.
    mtg: :py:class:`seminar.models.Meeting`
        The :py:class:`Meeting` to generate the Kaggle Kernel slug.

    Return
    ------
    slug: str
        The Kaggle InClass Competition slug. Viewable at kaggle.com/c/<slug>
    """
    return f"{cfg.settings.org_name}-{slug_kernel(cfg, mtg)}"
