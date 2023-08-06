Python client for PWBM-API

## Requirements
Tool implemented for Python version >= 3.8

## Installation instruction

### Install Python package:
Execute following command:
```shell
pip install pwbm-api-client
```

### Import package and use it
```python

from pwbm_api.client import Client
from pwbm_api import Series, Table
```

### Examples of usage:
```python

from pwbm_api.client import Client
from pwbm_api import Series, Table

client = Client()

# series filtration example
response = client.get(
    Series.query().filter(
        frequencies=['Annual'],
        relates_to_table=True,
        sources=['Internal Revenue Service'],
        tags=[{'name': 'Metric'}],
        uoms=['Items'],
        date_range='2015-12-31--2020-01-01'
    ).order_by(field='name', order='desc')  # permitted field name: 'name', 'uom', 'frequency', 'source', 'start_date', 'end_date'
)

for series in response:
    print(series)

# series search example by multiple search queries
response = client.get(
    Series.query(search_text=['Pennsylvania', 'Business Application']).filter(
        relates_to_table=True,
        sources=['Centers for Disease Control and Prevention'],
        frequencies=['Annual']
    ).filter(
        uoms=['Items'],
        tags=[{'name': 'State'}]
    ).order_by(
        field='name', order='desc'  # permitted field name: 'name', 'uom', 'frequency', 'source', 'start_date', 'end_date'
    )
)

for series in response:
    print(series)

# series search by neum example
response = client.get(
    Series.query(
        neum='Pneumonia and COVID-19 Deaths'
    ).filter(
        sources=['Centers for Disease Control and Prevention'],
        relates_to_table=True
    ).filter(
        frequencies=['Annual'],
        uoms=['People'],
        date_range='2020--2022'
    ).order_by(field='name')
    # permitted field name: 'name', 'uom', 'source', 'start_date', 'end_date', 'rowVer'
)

for series in response:
    print(series)

# get series by ids example
response = client.get(
    Series.query(
        ids=[
            '0e517322-c989-458f-8a45-aa69522a8f4a',
            '938ce0b1-6903-4ef4-9d46-de0cfca716b0',
        ]
    ).filter(
        sources=['Census Bureau'],
        frequencies=['Weekly Ending Sunday'],
        uoms=['Items'],
        date_range='2020-01-01--2020-06-01',
        tags=[{'name': 'Metric'}]
    ).order_by(field='name')
    # permitted field name: 'name', 'uom', 'source', 'start_date', 'end_date'
)

for series in response:
    print(series)

# tables filtration example
response = client.get(
    Table.query().filter(
        sources=['American Community Survey (ACS)']
    ).order_by(field='name')  # permitted field name: 'name', 'source'
)

for table in response:
    print(table)

# tables search example by multiple search queries
response = client.get(
    Table.query(
        search_text=['Pennsylvania', 'Place Of Work']
    ).filter(
        sources=['American Community Survey (ACS)']
    ).order_by(field='name', order='desc')  # permitted field name: 'name', 'source'
)

for table in response:
    print(table)

# get tables by ids example
response = client.get(
    Table.query(
        ids=['26bbc89d-26ba-4696-ba5a-a23ea2c1934e', '451dd022-204f-4fea-bf2f-f2650a09ea42']
    ).filter(
        sources=['American Community Survey (ACS)']
    ).order_by(field='source', order='asc')  # permitted field name: 'name', 'source'
)

for table in response:
    print(table)

# tables search by neum example
response = client.get(
    Table.query(
        neum='Pennsylvania'
    ).filter(
        sources=['Internal Revenue Service']
    ).order_by(field='name', order='desc')  # permitted field name: 'name', 'source', 'rowVer'
)

for table in response:
    print(table)

```