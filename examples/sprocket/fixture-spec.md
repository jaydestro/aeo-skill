# Sprocket fixture specification 0.1

This repository owns this fictional review exercise. Sprocket does not exist
as an Azure Cosmos DB feature. The term refers only to the local mock described
here; this is not Microsoft documentation, an SDK contract, or a product claim.

## Supported mock behavior

The simulator calculates how many batches are needed to group a specified
number of imaginary items. It performs integer arithmetic locally; it does not
read, write, index, or query a database. It does not allocate actual item batches.

| Input | Requirement |
|---|---|
| `--items` | Required integer from 1 to 1000, inclusive |
| `--batch-size` | Required integer from 1 to 32, inclusive |
| Python | Version 3.10 or later; standard library only |
| Working directory | Repository root for the documented relative command |
| Credentials/network | Neither is needed or used |

The batch count is `(items + batch_size - 1) // batch_size`.
Invalid/missing arguments produce an argparse error and nonzero exit status.
There is no `--mode`, `turbo`, cloud rollout, pricing, or state-changing operation.

## Reproducible example

```bash
python3 examples/sprocket/sprocket_demo.py --items 12 --batch-size 4
```

Expected JSON, ignoring object-key order:

```json
{"feature": "fictional-sprocket", "items": 12, "batch_size": 4, "batches": 3, "network_calls": 0}
```

The runnable implementation is [sprocket_demo.py](sprocket_demo.py).
Claims about faster Azure queries, zero RU charges, infinite scale, automatic
index changes, or availability in real accounts contradict this specification.
No performance benchmark or real cloud support is provided by this fixture.

## Media boundaries

The bad document intentionally refers to a missing image and an
`example.invalid` video URL. No recording exists in this fixture. The reference
rewrite uses an original SVG diagram and a clearly labeled text walkthrough.
Do not invent a video transcript or replace broken links with fabricated
Microsoft documentation.
