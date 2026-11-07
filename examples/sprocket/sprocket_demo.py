#!/usr/bin/env python3
"""Offline fictional Sprocket fixture; not an Azure Cosmos DB feature."""
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=int, required=True)
    parser.add_argument("--batch-size", type=int, required=True)
    args = parser.parse_args()
    if not 1 <= args.items <= 1000:
        parser.error("--items must be from 1 to 1000")
    if not 1 <= args.batch_size <= 32:
        parser.error("--batch-size must be from 1 to 32")
    print(json.dumps({
        "feature": "fictional-sprocket",
        "items": args.items,
        "batch_size": args.batch_size,
        "batches": (args.items + args.batch_size - 1) // args.batch_size,
        "network_calls": 0,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
