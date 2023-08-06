"""Notebooks are the bread-and-butter of teaching folks to code. This command group
provides a way to generate Solutionbooks then render them as:

* Workbooks, to enable interactive tutorial/self-study sessions.
* Markdown Posts, to enable publication on the web.

"""
import json
from typing import Union
from pathlib import Path

import click
from click import Context
import nbformat as nbf
from jinja2 import Template
from nbconvert.exporters import MarkdownExporter, NotebookExporter
from nbconvert.preprocessors import TagRemovePreprocessor
from nbgrader.preprocessors import ClearOutput, ClearSolutions

from seminar.utils import j2env, search
from seminar.models import Meeting
from seminar.apis import hugo
from seminar.commands import query_args, query_kwargs


@click.group(name="notebook")
@click.option(*query_args, **query_kwargs)
@click.pass_context
def cli(ctx, query: str = "") -> None:
    r"""Interact with a Meeting's Jupyter Notebooks.

    Specify the name of a :class:`seminar.models.Meeting` to perform operations over the notebooks
    related to said :class:`seminar.models.Meeting`.
    """
    search.for_meeting(ctx.obj, query)
    return None


def _default_notebook(ctx: Context, mtg: Meeting) -> nbf.NotebookNode:
    r""""""
    nb = nbf.v4.new_notebook()

    # Inject Heading
    html_header = j2env.get_template("notebooks/header.html.j2")
    banner_url = Template(ctx.obj.settings.hugo.banner_url).render(
        group=ctx.obj.group, meeting=mtg
    )
    header = html_header.render(banner_url=banner_url, meeting=mtg, group=ctx.obj.group)
    header_metadata = {"title": mtg.title, "tags": ["nb-title", "template"]}
    nb.cells.insert(0, nbf.v4.new_markdown_cell(header, metadata=header_metadata))

    # Inject data-loading cell
    from seminar.apis import kaggle

    py_dataset_path = j2env.get_template("notebooks/data-pathing.py.j2")
    dataset = py_dataset_path.render(slug=kaggle.slug_competition(ctx.obj, mtg))
    dataset_metadata = {"language": "python", "tags": ["template"]}
    nb.cells.insert(1, nbf.v4.new_code_cell(dataset, metadata=dataset_metadata))

    # Inject Notebook Metadata
    nb_metadata = j2env.get_template("notebooks/nb-metadata.json.j2")
    metadata = nb_metadata.render(meeting=mtg, group=ctx.obj.group)
    nb.metadata.update(json.loads(metadata))

    return nb


def _read_solutionbook(mtg: Meeting, path: Path) -> nbf.NotebookNode:
    r""""""
    standard = NotebookExporter()
    standard.register_preprocessor(
        TagRemovePreprocessor(remove_cell_tags=["template"]), enabled=True
    )

    nb, _ = standard.from_filename(str(path))
    nb = nbf.reads(nb, as_version=4)

    return nb


@cli.command()
@click.pass_context
def make_solutionbook(ctx, mtg: Meeting):
    r"""Ensures that all Solutionbooks have accurate headings, pathing, and metadata.

    **Solutionbooks** are the notebooks that make up a fully-complete workshop/lesson.
    Participants should be able to proceed through this notebook with no errors and
    achieve the expected [code] outcomes.

    """
    base_nb = _default_notebook(ctx, mtg)

    path = ctx.obj.path / mtg.solnbook
    # If the notebook doesn't exist, or it's empty
    if not path.exists() or path.stat().st_size == 0:
        nbf.write(base_nb, open(path, "w"))

    read_nb = _read_solutionbook(mtg, path)
    read_nb.cells = base_nb.cells + read_nb.cells[len(base_nb.cells) :]
    read_nb.metadata.merge(base_nb.metadata)

    nbf.write(read_nb, path.open("w"))


@cli.command()
@click.pass_context
def make_workbook(ctx, mtg: Meeting) -> None:
    r"""Generates a Workbook from a Solutionbook.

    Workbooks are stripped down Solutionbooks that, namely:

    * Have no output cells.
    * Replace ``### BEGIN SOLUTION ... ### END SOLUTION`` blocks with
      ``raise NotImplementedError()`` snippets for viewers to practice on.

    This enables participants to follow along during live teaching sessions or to work
    through the notebooks on their own time without exposure to the answers.

    .. todo: Migrate back to ``enforce_metadata=True``
    """
    workbook = NotebookExporter()

    preprocessors = [ClearOutput(), ClearSolutions(enforce_metadata=False)]
    for preprocessor in preprocessors:
        workbook.register_preprocessor(preprocessor, enabled=True)
    # TODO migrate back to `enforce_metadata=True`

    # workbook.register_preprocessor(ValidateNBGrader(), enabled=True)
    # this is only useful if we can migrate back to `enforce_metadata=True`

    try:
        nb, _ = workbook.from_filename(str(mtg.solnbook))
        nb = nbf.reads(nb, as_version=4)

        nbf.write(nb, mtg.workbook.open("w", encoding="utf-8"))
    except Exception:
        raise Exception(f"Workbook export failed on `{mtg}`.")


@cli.command()
@click.pass_context
def make_post(ctx: Context, mtg: Meeting, weight: int = -1) -> None:
    """Preprocess a Solutionbook and prepare it to post on the web."""
    as_post = MarkdownExporter(
        config={
            "extra_loaders": [j2env.loader],
            "template_file": "notebooks/to-post.md.j2",
            "no_prompt": True,
        }
    )
    as_post.register_preprocessor(
        TagRemovePreprocessor(remove_cell_tags=["nb-title"], enabled=True)
    )

    # Default to `git`-based "Last modified..."
    # lastmod = pd.Timestamp(name.stat().st_mtime, unit="s")
    # setattr(m, "lastmod", lastmod)

    try:
        nb, _ = as_post.from_filename(str(ctx.obj.path / mtg.solnbook))
    except FileNotFoundError:
        return False

    if not diff_notebook(ctx, mtg):
        return False

    ctx.invoke(hugo.touch_meeting, mtg=mtg, body=nb, weight=weight, from_nb=True)

    return True


def diff_notebook(ctx: Context, mtg: Meeting) -> bool:
    tmpl = _default_notebook(ctx, mtg)

    standard = NotebookExporter()
    disk, _ = standard.from_filename(str(mtg.solnbook))
    disk = nbf.reads(disk, as_version=4)

    return tmpl != disk


@cli.command()
@click.pass_context
def kaggle_metadata(ctx: Context, mtg: Meeting):
    r"""TODO docstring"""
    if not diff_notebook(ctx, mtg):
        return

    from seminar.apis import kaggle

    ctx.invoke(kaggle.kernel_metadata, mtg=mtg)


@cli.command()
@click.pass_context
def push_kaggle(ctx: Context, mtg: Meeting):
    r"""TODO docstring"""
    if not diff_notebook(ctx, mtg):
        return

    from seminar.apis import kaggle

    ctx.invoke(kaggle.push_kernel, mtg=mtg)


@click.command()
@click.pass_context
def cleanup(ctx: Context, mtg: Meeting) -> None:
    r"""TODO docstring"""
    tmpl = _default_notebook(ctx, mtg)

    try:
        disk = _read_solutionbook(mtg, mtg.solnbook)
    except (FileNotFoundError, nbf.NBFormatError):
        return

    rm = False
    rm = len(disk.cells) == 0 or tmpl.cells == disk.cells

    if rm:
        mtg.solnbook.unlink()
        mtg.workbook.unlink(missing_ok=True)
        mtg.kernel.unlink(missing_ok=True)
