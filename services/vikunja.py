import requests

from config import settings
from models.task import Task


class VikunjaService:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = settings.internal_ca
        self.session.headers.update({
            "Authorization": f"Bearer {settings.vikunja_api_key}"
        })

        self.base_url = settings.vikunja_url.rstrip("/")
        self._project_lookup = None

    def get_tasks(self):
        response = self.session.get(f"{self.base_url}/tasks")
        response.raise_for_status()
        return response.json()

    def get_projects(self):
        response = self.session.get(f"{self.base_url}/projects")
        response.raise_for_status()
        return response.json()

    def get_project_lookup(self):
        if self._project_lookup is None:
            self._project_lookup = {
                project["id"]: project["title"]
                for project in self.get_projects()
            }

        return self._project_lookup

   

    def get_open_tasks(self):
        projects = self.get_project_lookup()

        tasks = []

        for task in self.get_tasks():
            if task["done"]:
                continue

            task_copy = task.copy()
            task_copy["project"] = projects.get(
                task["project_id"],
                f"Unknown ({task['project_id']})"
            )

            tasks.append(
                Task(
                    id=task["id"],
                    title=task["title"],
                    project=projects[task["project_id"]],
                    done=task["done"],
                )
            )

        return tasks