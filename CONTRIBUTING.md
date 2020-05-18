## Development and Contributing

## Issue

To make an improvement, add a new feature or anything else, please open a issue first.

## Setup

Then by setting up and activating a virtualenv:

```
git clone git@github.com:hakancelik96/unimport.git
cd unimport
python3 -m venv env
source env/bin/activate
pip install --upgrade pip # optional, if you have an old system version of pip
pip install -r requirements.txt -r requirements-dev.txt
git checkout -b i{your issue number}
```

## Commit messages

If you want, you can use the emoji about the commit message you will throw, this can
help us better understand the change you have made and also it is fun.

- When you make any support commit; 💪
- When you make any tests commit; 🧪
- When you make any fix commit; 🐞
- When you make any optimizasiyon commit; 💊

## Formatting

We use isort, black and of course unimport to format code. To all format changes to be
conformant, run the following in the root:

```
pre-commit run --all-files
```

## Testing

You can run the tests by typing the following command.

```
python -m unitttest
```

## License

Unimport is MIT licensed, as found in the LICENSE file.
