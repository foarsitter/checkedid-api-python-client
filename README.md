# CheckedID Python API client

[![PyPI](https://img.shields.io/pypi/v/checkedid.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/checkedid.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/checkedid)][python version]
[![License](https://img.shields.io/pypi/l/checkedid)][license]

[![Read the documentation at https://checkedid.readthedocs.io/](https://img.shields.io/readthedocs/checkedid-api-python-client/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/foarsitter/checkedid-api-python-client/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/foarsitter/checkedid-api-python-client/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/checkedid/
[status]: https://pypi.org/project/checkedid/
[python version]: https://pypi.org/project/checkedid
[read the docs]: https://checkedid.readthedocs.io/
[tests]: https://github.com/foarsitter/checkedid-api-python-client/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/foarsitter/checkedid-api-python-client
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

- Typed API client for api.checkedid.eu

## Requirements

- Build with Pydantic and httpx, does currently not support async.

## Installation

You can install _CheckedID Python API client_ via [pip] from [PyPI]:

```console
$ pip install checkedid
```

## Usage

```py
from checkedid import errors, models, Client

try:
    client = Client('1001')
    dossier: models.ReportResponse = client.dossier('123456789')
except errors.CheckedIDNotFoundError as e:
    print("Dossier does not exists")
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_CheckedID Python API client_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/foarsitter/checkedid-api-python-client/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/foarsitter/checkedid-api-python-client/blob/main/LICENSE
[contributor guide]: https://github.com/foarsitter/checkedid-api-python-client/blob/main/CONTRIBUTING.md
