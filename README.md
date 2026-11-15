# uuidgen

Generate and inspect UUIDs from your terminal. Zero dependencies, pure Python stdlib.

## Install

```bash
pip install uuidgen-cli
```

Or run directly:

```bash
python uuidgen.py --help
```

## Usage

```bash
# Generate a v4 UUID
uuidgen

# Generate v7 (time-ordered)
uuidgen -v 7

# Generate 5 UUIDs
uuidgen -n 5

# Generate v5 (name-based)
uuidgen gen -v 5 --namespace dns --name example.com

# Parse a UUID
uuidgen parse 550e8400-e29b-41d4-a716-446655440000

# Validate
uuidgen validate 550e8400-e29b-41d4-a716-446655440000
```

## Versions

1, 4, 5, 7

## License

MIT