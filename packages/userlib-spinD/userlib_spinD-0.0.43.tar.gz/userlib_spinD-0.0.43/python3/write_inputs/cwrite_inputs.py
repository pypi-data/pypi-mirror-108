# -*- coding: utf-8 -*-
r"""
This module takes care of writing input files for calculations with the SpinD-code
"""
from typing import TypeVar, List
from pathlib import Path
from python3.shell_commands import adjust_parameter

PathLike = TypeVar("PathLike", str, Path)


class CWriteInput:
    r"""
    General class for writing input files
    """

    def __init__(self, file: str, **kwargs) -> None:
        r"""
        Initializes writing of input file

        Args:
            name(str): name of the created file
        """
        self.file = file
        self.content = dict(**kwargs)
        self.contentlines = []

    def __call__(self, where: Path = Path.cwd()) -> None:
        r"""
        Calls the writing
        """
        self.where = where
        with open(str(where / self.file), 'a') as f:
            for (key, value) in self.content.items():
                f.write(key + ' ' + value + '\n')
            for line in self.contentlines:
                f.write(line + '\n')

    def appendline(self, value: str) -> None:
        r"""
        Appends a line to the input file
        """
        self.contentlines.append(value)

    def appendmultilinevalues(self, key: str, values: List[str]) -> None:
        r"""
        Some input files have multiple lines of values after a key line. E. g. lattice in lattice in. In this case
        provide the key line as key and each following line in a list of strings
        """
        with open(str(self.where / self.file), 'a') as f:
            f.write(key + '\n')
            for line in values:
                f.write(line + '\n')

    def replaceline(self, key: str, value: str) -> None:
        r"""
        Replaces the line addressed by key with key + value
        """
        adjust_parameter(keyword=key, value=value, directory_file=self.file)
