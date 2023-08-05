# Poetry issues

## Poetry could not be installed even if removed from path

Context:
- Poetry removed from path
- Trying to install poetry using `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

Observed error:
- Log saying poetry is already installed in the latest version event if this is not the case

How to fix:

```bash
mv ~/.poetry ~/.poetry.backup
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

## Poetry issues an error about Cleo

Usually, it happens when poetry has been upgraded from a version not compatible with the one that replaces it.

The solution is to uninstall and reinstall poetry:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --uninstall
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
