## Development and Contributing

## Issue

To make an improvement, add a new feature or anything else, please open a issue first.

## Fork Repository

[fork the unimport.](https://github.com/hakancelik96/unimport/fork)

## Clone Repository

```bash
$ git clone git@github.com:<USERNAME>/unimport.git
$ cd unimport
```

## Setup Python

Then by setting up and activating a virtualenv:

```bash
$ python3.8 -m venv env #python3.6, python3.7 or python3.8
$ source env/bin/activate
$ pip install --upgrade pip # optional, if you have an old system version of pip
$ pip install -r requirements.txt -r requirements-dev.txt
git checkout -b i{your issue number}
```

## Install pre-commit hooks

```bash
$ pre-commit install # to pre-commit will run automatically on git commit!
```

## How to Update My Local Repository

```bash
$ git remote add upstream git@github.com:hakancelik96/unimport.git
$ git fetch upstream # or git fetch --all
$ git rebase upstream/master
```

## Code

After adding a new feature or fixing a bug please report your change to
[CHANGELOG.md](/CHANGELOG.md)

### Commit Messages

If you want, you can use the emoji about the commit message you will throw, this can
help us better understand the change you have made and also it is fun.

- When you make any support commit; 💪
- When you make any tests commit; 🧪
- When you make any fix commit; 🐞
- When you make any optimizasiyon commit; 💊

## Testing

You can run the tests by typing the following command.

```python
python -m unittest
```

## License

Unimport is MIT licensed, as found in the LICENSE file.
