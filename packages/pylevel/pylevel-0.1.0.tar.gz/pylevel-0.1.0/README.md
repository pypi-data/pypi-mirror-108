# pylevel

PyLevel is a LevelDB driver for python.
It use rust reimplementation of LevelDB https://docs.rs/rusty-leveldb .

## Requirements

- python3.8+
- Rust https://www.rust-lang.org/

## Install

```
$ sudo apt-get install python3-dev
$ pip install pylevel
```

## Example

### simple put/get/delete
```
import pylevel
db = pylevel.DB("/tmp/testdb", create_if_missing=True)

db.put(b'key', b'value')
v = db.get(b'key')      # 'value'

db.delete(b'key')
v = db.get(b'key')      # None

db.close()
```
