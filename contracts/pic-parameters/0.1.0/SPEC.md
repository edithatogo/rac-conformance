# pic-parameters 0.1.0

`pic-parameters` records temporal policy parameters as immutable value periods. Supersession is represented by adding a new period, never by changing an old one.

## File Shape

```json
{
  "conformsTo": "pic-parameters/0.1.0",
  "parameters": []
}
```

Each parameter has:

- `id`: a package-scoped PIC ID.
- `label`: human-readable label.
- `unit` or `currency`: the measurement unit. Money parameters use `currency`.
- `values`: ordered, non-overlapping periods.
- `calendar`: timezone and convention.
- `rounding`: optional rounding declaration from `pic-semantics`.

## Values

`value` may be:

- a decimal string,
- an integer,
- a boolean,
- an enum string,
- a schedule table: `{"brackets": [{"threshold": "0", "rate": "0.10"}]}` or `amount`.

Binary floating-point numbers are invalid. Decimal money and rates are strings.

## Period Rules

`values` must be ordered by `from`. Periods must not overlap. `to: null` means open-ended and must be the final period. JSON Schema validates the shape; `pic_contracts.parameters.validate_parameter_periods` validates ordering and overlap.

