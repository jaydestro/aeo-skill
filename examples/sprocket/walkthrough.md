# Fictional Sprocket text-only walkthrough

This is an authored text demonstration of fixture version 0.1, not a transcript
of an actual video. Sprocket is not a real Azure Cosmos DB feature.
The [local specification](fixture-spec.md) is the source of truth.

1. Use Python 3.10+ at this repository's root; no Azure credentials are needed.
2. Run the offline calculation:

   ```bash
   python3 examples/sprocket/sprocket_demo.py --items 12 --batch-size 4
   ```

3. Read the JSON result: `feature` is `fictional-sprocket`, `batches` is `3`,
   and `network_calls` is `0`.
4. Interpret the arithmetic as three groups of four imaginary items. No actual
   database items or resources are created, so there is no cleanup.

Both arguments are required; `--items` accepts 1-1000 and `--batch-size` accepts
1-32. Unknown, missing, non-integer, or out-of-range arguments fail explicitly.
The mock says nothing about RU costs or query speed. See
[the reference article](after.md) for the full explanation.
