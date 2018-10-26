# Simplified_Google_Sheets

Google Sheet API wrapper for simplified and common tasks.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python 3.x

### Installing

To install use command line:

```
pip install git+https://github.com/FrancoJim/Simplified_Google_Sheets.git
```

### Examples of Usage

#### To add a lists nested in a single list - i.e. "[ [ ], [ ] , ]" - to a Google Sheets spreadsheet.
Once the data is in a list of nested list format, a single line can import a spreadsheet into a Google Sheets workbook.

```
import simplfied_google_sheets.sheets import as gs

sample_data =   [
                ["Row 1", "Row 1", "Row 1",],
                ["Row 2", "Row 2", "Row 2",],
                ["Row 3", "Row 3", "Row 3",],
                ]

gs.import_to_gsheets(workbook="Sample Workbook", spreadsheet="List of Rows", data=sample_data, api_json=GGLJSONAUTH, share_spreadsheet="user@gmail.com")
```

#### To balance nested lists within list.

```
import simplfied_google_sheets.sheets import as gs

sample_data =   [
                ["Row 1", "Row 1", "Row 1", "Row 1", "Row 1", ],
                ["Row 2", "Row 2", "Row 2", "Row 2", "Row 2", "Row 2", "Row 2", "Row 2", ],
                ["Row 3", "Row 3", ],
                ]

spreadsheet_cell_ready = gs.balance_rows(sample_data)

print(spreadsheet_cell_ready)

Output:
[['Row 1', 'Row 1', 'Row 1', 'Row 1', 'Row 1', '', '', ''], ['Row 2', 'Row 2', 'Row 2', 'Row 2', 'Row 2', 'Row 2', 'Row 2', 'Row 2'], ['Row 3', 'Row 3', '', '', '', '', '', '']]
```

#### Convert Dictionary to list of nested lists (Spreadsheet Format)

```
from simplfied_google_sheets.sheets import *

sample_data =   [
                {'key1': 'Value 1', 'key2': 'Value 2', 'key3': 'Value 3', },
                {'key1': 'Value 4', 'key2': 'Value 5', 'key3': 'Value 6', },
                ]

spreadsheet_cell_ready = dict_to_spreadsheet_format(sample_data, include_header=True)

print(spreadsheet_cell_ready)

Output:
[['key3', 'key1', 'key2'], ['Value 3', 'Value 1', 'Value 2'], ['Value 6', 'Value 4', 'Value 5']]
```

## Built With

* [burnash/gspread](https://github.com/burnash/gspread) - Google Spreadsheets Python API

## Contributing

* [@FrancoJim](https://github.com/FrancoJim) (Kevin Lang)

## Authors

* **Kevin Lang** - *Initial work* - [@FrancoJim](https://github.com/FrancoJim)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

