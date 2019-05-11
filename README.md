### Usage

```
python3 main.py [-analysisMethod] [-typeOfOrder]
```

Available options for ```-analysisMethod```:

- -reglin (linear regression (best-fit))
- -quart (quartiles)

Available options for ```-typeOfOrder```:

- -first (fetch top ranked athletes)
- -last (fetch last ranked athletes)
- -random (fetch random athletes)

Run ```python3 main.py -h``` for more information.

### Dependencies

- NumPy
- pandas
- scikit-learn