import sys
import time
from typing import Optional

from looker_sdk import client, models

sdk = client.setup("../looker.ini")


def main():
    dashboard_title = sys.argv[1] if len(sys.argv) > 1 else ""
    pdf_style = sys.argv[2] if len(sys.argv) > 2 else "tiled"
    pdf_width = int(sys.argv[3]) if len(sys.argv) > 3 else 545
    pdf_height = int(sys.argv[4]) if len(sys.argv) > 4 else 842

    if not dashboard_title:
        print(
            "Please provide: <dashboardTitle> [<dashboard_style>] [<pdf_width>] [<pdf_height>]"
        )
        print('  dashboard_style defaults to "tiled"')
        print("  pdf_width defaults to 545")
        print("  pdf_height defaults to 842")
        return

    dashboard = get_dashboard(dashboard_title)
    if dashboard:
        download_dashboard(dashboard, pdf_style, pdf_width, pdf_height)


def get_dashboard(title: str) -> Optional[models.Dashboard]:
    """Get a dashboard by title."""
    title = title.lower()
    dashboard = next(iter(sdk.search_dashboards(title=title)), None)
    if not dashboard:
        print(f'Dashboard "{title}" was not found.')
    return dashboard


def download_dashboard(
    dashboard: models.Dashboard, style: str, width: int, height: int
):
    """Download specified dashboard as PDF."""
    assert dashboard.id
    id = int(dashboard.id)
    task = sdk.create_dashboard_render_task(
        id,
        "pdf",
        models.CreateDashboardRenderTask(dashboard_style=style),
        width,
        height,
        pdf_paper_size="A4",
    )

    if not (task and task.id):
        print(f"Could not create a render task for {dashboard.title}")
        return

    # poll the render task until it completes
    elapsed = 0.0
    delay = 0.5  # wait .5 seconds
    while True:
        poll = sdk.render_task(task.id)
        if poll.status == "failure":
            print(poll)
            print(f"Render failed for {dashboard.title}")
            return
        elif poll.status == "success":
            break

        time.sleep(delay)
        elapsed += delay
    print(f"Render task completed in {elapsed} seconds")

    result = sdk.render_task_results(task.id)
    filename = f"{dashboard.title}.pdf"
    with open(filename, "wb+") as f:
        f.write(result)
    print(f"Dashboard pdf saved to {filename}")


main()
