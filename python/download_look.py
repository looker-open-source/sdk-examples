import sys
import time
from looker_sdk import client, models, error
sdk = client.setup("looker.ini")
def main():
    look_title = "INSERT TITLE"
    look_width = 1000
    look_height = 1000
    look = get_look(look_title)
    download_look(look, look_width, look_height)
    
    
def get_look(title: str) -> models.Look:
    title = title.lower()
    look = next(iter(sdk.search_looks(title = title)), None)
    if not look:
        print(f"look {title} was not found")
    assert isinstance(look, models.Look)
    return look
    
def download_look(
    look: models.Look, width: int, height: int
    ):
    """Download specified look as PNG."""
    assert look.id
    id = int(look.id)
    task = sdk.create_look_render_task(
        id,
        "png",
        width,
        height,
        )
    if not (task and task.id):
        print(f"Could not create a render task for {look.title}")
        return None
        
    # poll the render task until it completes
    elapsed = 0.0
    delay = 0.5  # wait .5 seconds
    while True:
        poll = sdk.render_task(task.id)
        if poll.status == "failure":
            print(poll)
            print(f"Render failed for {look.title}")
            return None
        elif poll.status == "success":
            break
        time.sleep(delay)
        elapsed += delay
    print(f"Render task completed in {elapsed} seconds")
    result = sdk.render_task_results(task.id)
    fileName = f"{look.title}" + "_look.png"
    with open(fileName, "wb+") as f:
        f.write(result)
    print(f"PNG saved to {fileName}")
main()