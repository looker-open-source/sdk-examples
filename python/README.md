# Python Examples for the Looker API

You can find Python language examples in this folder. 

NOTE: Due to changes from version 0.1.3b8, older examples have been moved to [an archive folder](v0_1_3b7__and_earlier). Code using the older syntax can be identified by use of the `from looker_sdk import client` import, and `sdk = client.setup()` initialization command. Up to date code will use the `sdk = looker_sdk.initXX()` syntax.

## Run queries

- [Define a query with a JSON body](run_inline_query.py)

## Looker administration

- [Get a data dictionary for an explore](lookml_model_explore.py)
- [Assign groups to a role](assign_groups_to_role.py)
- [Disable users by email](disable_users_by_email.py)

# Previous SDK syntax

## Connection management

- [Test a specified connection](test_connection.py)

## Manage Dashboards

- [Soft delete dashboard](soft_delete_dashboard.py)

## Manage Render Tasks

- [Download dashboard tile in specified format](download_tile.py)
- [Download look in specified format](download_look.py)
- [Generate and download dashboard PDFs](download_dashboard_pdf.py)

## User Management

- [Disable all active user sessions](logout_all_users.py)
