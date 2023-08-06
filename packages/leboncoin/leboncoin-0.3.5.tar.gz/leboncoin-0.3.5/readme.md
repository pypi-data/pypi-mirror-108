# Leboncoin

Access Leboncoin api in Python

## Installation
```bash
pip install leboncoin
```

## Usage

```python
from leboncoin import Leboncoin

lbc = Leboncoin()
lbc.searchFor("iphone")
lbc.setLimit(10)
lbc.maxPrice(2000)
lbc.setDepartement("tarn")
results = lbc.execute()

for ad in results["ads"]:
    print(ad["subject"], ad["price"])
print("\n")
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)