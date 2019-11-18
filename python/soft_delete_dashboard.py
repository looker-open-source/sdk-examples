import sys
import time

from looker_sdk import client, models


sdk = client.setup("looker.ini")

def main():
        ### INSERT TITLE HERE #####
        dashboard_title = "LAST_TRY"
   

        if not dashboard_title:
            print(
                "Please provide: <dashboardTitle> "
            )
            return

        dashboard = get_dashboard(dashboard_title)
        delete_dashboard(dashboard)

#### GET DASHBOARD OBJECT #####
def get_dashboard(title: str) -> models.Dashboard:
        """Get a dashboard by title"""
        title = title.lower()
        dashboard = next(iter(sdk.search_dashboards(title=title)), None)
        if not dashboard:
            print(f"dashboard {title} was not found")
        assert isinstance(dashboard, models.Dashboard)
        return dashboard


def delete_dashboard(
        dashboard: models.Dashboard,
    ):
        """Download specified dashboard as PDF."""
        assert dashboard.id
        id = int(dashboard.id)
        ### ID SHOULD BE THE SAME AS IN URL OF DASHBOARD YOU ARE ATTEMPTING TO DELETE ###
        #print(id)

        task = sdk.delete_dashboard(
            id
        )


main()