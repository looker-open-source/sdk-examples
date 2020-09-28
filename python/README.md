# Python Examples for the Looker API

You can find Python language examples in this folder.

### General examples

|  &nbsp;&nbsp;Example&nbsp;Topic&nbsp;&nbsp; | Discussion |
| ------------- | ---------- |
| [custom config reader](custom_config_reader.py) | Shows how to implement a custom method of reading your configuration settings, including API credentials |

## Connection management
|  &nbsp;&nbsp;Example&nbsp;Topic&nbsp;&nbsp; | Discussion |
| ------------- | ---------- |
| [Testing a connection](test_connection.py) | Shows how to obtain and run all supported tests for a given connection name.|


## Manage Dashboards
|  &nbsp;&nbsp;Example&nbsp;Topic&nbsp;&nbsp; | Discussion |
| ------------- | ---------- |
| [Soft delete dashboard](soft_delete_dashboard.py)| Shows how to look up a dashboards by title and move them to the trash folder. |


## Manage Render Tasks
|  &nbsp;&nbsp;Example&nbsp;Topic&nbsp;&nbsp; | Discussion |
| ------------- | ---------- |
| [Download dashboard tile in specified format](download_tile.py) | Find the requested dashboard by name, then the requested tile by name. If either name matches, the list of all available items is display. Supported output formats are PNG, JPG, CSV, JSON, and anything else supported by the `run_query` endpoint. This sample shows progress during a render task. |
| [Download look in specified format](download_look.py) | Find the requested look by name, create a render task and write the binary result to file. |
| [Generate and download dashboard PDFs](download_dashboard_pdf.py) | Find the requested dashboard by name, create a render task and write the binary result to file. |

## User Management
|  &nbsp;&nbsp;Example&nbsp;Topic&nbsp;&nbsp; | Discussion |
| ------------- | ---------- |
| [Disable all active user sessions](logout_all_users.py) | Shows how to iterate through all users and terminate any active sessions they might have. |
