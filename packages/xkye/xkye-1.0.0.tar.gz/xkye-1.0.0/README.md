# Xkye Python Library

Introducing **Xkye-Python** standard library to provide objective query builder for [xkye language](https://github.com/RahmanAnsari/xkye-lang). You can easily query the entities from the xkye file using this library. It provides a more convenient and idiomatic way to write and manipulate queries.

</br>

![Travis (.com)](https://img.shields.io/travis/com/RahmanAnsari/xkye_python?style=for-the-badge&labelColor=000000)
![Codecov](https://img.shields.io/codecov/c/github/RahmanAnsari/xkye_python?style=for-the-badge&labelColor=000000)
![CodeStyle](https://img.shields.io/badge/code%20style-black-black?style=for-the-badge&labelColor=000000)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/RahmanAnsari/xkye_python?style=for-the-badge&labelColor=000000)
![Read the Docs](https://img.shields.io/readthedocs/xkye-python?style=for-the-badge&labelColor=000000)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge&labelColor=000000)

</br>

## Installation

Install library with [pypi](https://pypi.org/):

```sh
$ pip3 install xkye
```

</br>

## Usage
```sh
from xkye import IO as io

#initiate the xkye with io
x = io(filename.xky)

#read the contents of the file
x.read()

#get the output of any of the entity from teh xky file
#to get the value of the entity
x.get("entityname")

#to get the value of the entity in the given clutch
x.get("entityname","clutchname")

#to get the value of the entity in the given cluth's span
x.get("entityname","clutchname", clutchspan)
```

</br>

## Examples
Please see the [examples](https://github.com/RahmanAnsari/xkye_python/tree/main/examples) directory to see some complex examples using xkye-pyhton. For details about xkye syntax and format, use the offical [Xkye-lang](https://github.com/RahmanAnsari/xkye-lang) repo.

</br>

## Documentation
Documentation is available at [xkye-python.readthedocs.io](https://xkye-python.readthedocs.io/en/latest/).

</br>

## Version matrix

| [Xkye version](https://github.com/RahmanAnsari/xkye-lang) | [Xkye-Python Library version](https://github.com/RahmanAnsari/xkye_python)    |
| --------------------- | --------------------------- |
| >= [1.0.0](https://github.com/RahmanAnsari/xkye-lang/releases/tag/v1.0.0)               | >= [1.0.0](https://github.com/RahmanAnsari/xkye_python/releases/tag/v1.0.0)                      |

</br>

## Development
Clone this repository
```sh
git clone https://github.com/RahmanAnsari/xkye_python.git
```

Activate Virtual Environment ([virtualenv](https://pypi.org/project/virtualenv/)):

```sh
$ virtualenv venv
$ source venv/bin/activate
```

To install all of the dependencies necessary for development, run:
```sh
$ make dev
```

To run all of the tests for xkye-python, run:

```sh
$ pytest xkye
```

Alternatively, it is possible to use the run tests using make file, which wraps pytest.
```sh
$ make test
```

</br>

## Upcoming features on or before v2.0.0
- Ability to add entity, clutch and subclutch

</br>

## Code of conduct
This project and everyone participating in it will be governed by the [Xkye Code of Conduct](https://github.com/RahmanAnsari/xkye_python/blob/main/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to my email.

</br>

## Contribution Guide
Want to hack on Xkye-Python? Awesome! We have [Contribution-Guide](CONTRIBUTING.md). If you are not familiar with making a pull request using GitHub and/or git, please read [this guide](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests). If you're looking for ways to contribute, please look at our [issue tracker](https://github.com/RahmanAnsari/xkye_python/issues).

</br>

## License
Xkye-python is open-source standard python library for xkye language that is released under the MIT License. For details on the license, see the [LICENSE](LICENSE) file.

If you like this library, help me to develop it by buying a cup of coffee

<a href="https://www.buymeacoffee.com/rahmanansari" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" align="center"  alt="Buy Me A Coffee" height="41" width="174"></a>

