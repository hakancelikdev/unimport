## Development and Contributing

## Issue

To make an improvement, add a new feature or anything else, please open a issue first.

**Good first issues are the issues that you can quickly solve, we recommend you take a
look.**
[Good first issue](https://github.com/hakancelikdev/unimport/labels/good%20first%20issue)

## Fork Repository

[fork the unimport.](https://github.com/hakancelikdev/unimport/fork)

## Clone Repository

```shell
$ git clone git@github.com:<USERNAME>/unimport.git
$ cd unimport
```

## Setup Branch

```shell
git checkout -b i{your issue number}
```

## How to Update My Local Repository

```shell
$ git remote add upstream git@github.com:hakancelikdev/unimport.git
$ git fetch upstream # or git fetch --all
$ git rebase upstream/main
```

## Testing

First, make sure you have at least one of the python versions py3.8, py3.9, py3.10,
py3.11 and py3.12 If not all versions are available, after opening PR, github action
will run the tests for each version, so you can be sure that you wrote the correct code.
You can skip the tox step below.

After typing your codes, you should run the tests by typing the following command.

```shell
$ python3.12 -m pip install tox
$ tox
```

If all tests pass.

## The final step

After adding a new feature or fixing a bug please report your change to
[CHANGELOG.md](CHANGELOG.md) and write your name, GitHub address, and email in the
[AUTHORS.md](AUTHORS.md) file in alphabetical order.

## License

Unimport is MIT licensed, as found in the LICENSE file.
