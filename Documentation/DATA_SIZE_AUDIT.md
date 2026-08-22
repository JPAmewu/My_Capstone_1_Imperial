# Dataset-size audit

The repository was audited for `.npy`, `.npz`, `.csv`, `.tsv`, `.parquet`, `.pkl`, `.pickle`, and `.joblib` files. The audit applies a conservative 50 MiB warning threshold and the standard 100 MiB hard per-file Git hosting limit. Files at or above either threshold fail the automated check.

## Result

| Measure | Audited result |
| --- | ---: |
| Dataset files | 356 |
| `.npy` files | 240 |
| Total dataset size | 701,580 bytes (0.669 MiB) |
| Largest dataset | `Results/gp_rolling_validation_predictions.csv` |
| Largest file size | 48,568 bytes (0.046 MiB) |
| Files at or above 50 MiB | 0 |
| Files at or above 100 MiB | 0 |

The repository therefore does not contain a large dataset under either threshold, and Git LFS or an external data host is not required for the current evidence. The machine-readable file-by-file result is [`Results/dataset_size_audit.csv`](../Results/dataset_size_audit.csv). Re-run the gate with:

```bash
python Code/audit_dataset_sizes.py
```

This audit concerns storage size only. It does not replace the datasheet’s checks for array alignment, provenance, valid bounds, or evidence status.
