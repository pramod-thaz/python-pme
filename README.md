# python pme

Utility functions and sample usage for calculation of Private Equity PME measures using Python.


Usage:

```python
import pandas as pd
from pme import pme_calc
pme_calc(dataframe, end_date)
```
See accompanying Jupyter Notebook for detailed example

dataframe: A Pandas dataframe with a datetime index with atleast 3 columns (exact names): nav, cash_flow & bench

end_date: End Date or As-Of date for analysis

Credits: 
1. https://github.com/karlpolen/pme-calcs
2. https://github.com/Maween/PyPME
