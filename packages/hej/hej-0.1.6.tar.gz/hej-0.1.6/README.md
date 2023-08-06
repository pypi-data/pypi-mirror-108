A collection of useful tools.

## Install
```sh
python -m pip install hej
```

## Usage
```sh
python -m hej.files -h

# with files in the [a] that are not in the [b].
python -m hej.files sub tmp/a -b tmp/b -o tmp/z -i '.jpg,.xml'
```

published with [Flit](https://flit.readthedocs.io/en/latest/).