# Copyright 2024 Marimo. All rights reserved.
from __future__ import annotations

import os
import sys
import tempfile
import textwrap
from typing import TYPE_CHECKING

import pytest

from marimo._ast import codegen
from marimo._cli.convert.ipynb import convert_from_ipynb_file

if TYPE_CHECKING:
    from collections.abc import Sequence

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def get_codes(ipynb_name: str) -> tuple[Sequence[str], Sequence[str]]:
    contents = convert_from_ipynb_file(
        DIR_PATH + f"/ipynb_data/{ipynb_name}.ipynb.txt"
    )

    tempfile_name = ""
    try:
        # in windows, can't re-open an open named temporary file, hence
        # delete=False and manual clean up
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            tempfile_name = f.name
            f.write(contents)
            f.seek(0)
        app = codegen.get_app(f.name)
        assert app is not None
        cell_manager = app._cell_manager
        return list(cell_manager.codes()), list(cell_manager.names())
    finally:
        os.remove(tempfile_name)


def test_markdown() -> None:
    codes, names = get_codes("markdown")

    assert len(codes) == 3
    assert (
        codes[0]
        == textwrap.dedent(
            """
            mo.md(
                r\"\"\"
                # Hello, markdown

                \\"\\"\\"
                'hello"
                '''
                \\"\\"\\"
                \"\"\"
            )
            """
        ).strip()
    )
    assert (
        codes[1]
        == textwrap.dedent(
            """
            mo.md(
                r\"\"\"
                Here is some math

                $x \\approx 0$
                \"\"\"
            )
            """
        ).strip()
    )
    assert codes[2] == "import marimo as mo"
    assert [name == "_" for name in names]


def test_arithmetic() -> None:
    codes, names = get_codes("arithmetic")

    assert len(codes) == 2
    assert codes[0] == "x = 0\nx"
    assert codes[1] == "x + 1"
    assert names == ["__", "__"]


def test_blank() -> None:
    codes, names = get_codes("blank")

    assert len(codes) == 1
    assert codes[0] == ""
    assert names == ["__"]


def test_unparsable() -> None:
    codes, names = get_codes("unparsable")

    assert len(codes) == 2
    assert codes[0] == "!echo hello, world\n\nx = 0"
    assert codes[1] == "x"
    assert names == ["__", "__"]


@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="Feature not supported in python 3.8"
)
def test_multiple_defs() -> None:
    codes, _ = get_codes("multiple_defs")

    assert len(codes) == 7
    assert codes[0] == "_x = 0\n_x"
    assert codes[1] == "_x = 1\n_x"
    assert codes[2] == "y = 0"
    assert codes[3] == "y_1 = 1"
    assert codes[4] == "y_1"
    assert (
        codes[5]
        == textwrap.dedent(
            """
            for _i in range(3):
                print(_i)
            """
        ).strip()
    )
    assert (
        codes[6]
        == textwrap.dedent(
            """
            for _i in range(4):
                print(_i)

            """
        ).strip()
    )
