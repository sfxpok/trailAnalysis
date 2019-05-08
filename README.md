### Usage

```
python3 tkdk.py [-filter] [numberOfPeople]
```

Available options for ```-filter```:

- -f (fetch first ```numberOfPeople``` rows)
- -l (fetch last ```numberOfPeople``` rows)
- -r (fetch random ```numberOfPeople``` rows)
- -q (calculate global performance of a competition)

```numberOfPeople``` argument can only be an positive integer.

### Dependencies

- NumPy
- pandas
- scikit-learn