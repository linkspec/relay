from services.vikunja import VikunjaService
from tools.registry import register

_service = VikunjaService()


@register
def list_open_tasks() -> str:
    """
    Return all open tasks in a human-readable format.
    """
    tasks = _service.get_open_tasks()

    if not tasks:
        return "You have no open tasks."

    return "\n".join(
        f"[{task.project}] {task.title}"
        for task in tasks
    )