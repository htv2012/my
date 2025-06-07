# Function `PrettyTable.get_string()`

## Common `kwargs`

| Name        | Type     | Description                                           | Example               |
|-------------|----------|-------------------------------------------------------|-----------------------|
| border      | bool     | Include border?                                       | border=False          |
| fields      | list     | List of fields                                        | fields=["id", "name"] |
| header      | bool     | Include header?                                       | header=False          |
| reversesort | bool     | Reverse sorting?                                      | reversesort=True      |
| sortby      | str      | Name of field to sort by                              | sortby="name"         |
| sort_key    | callable | Function which take a row and return the sorted field |                       |
| start       | int      | Start row, 1 based                                    | start=1               |
| stop        | int      | The end row                                           | end=10                |

