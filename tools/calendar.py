from services.calendar import CalendarService

class CalendarTool:

    name = "calendar"

    def __init__(self):
        self.service = CalendarService()

    
    @property
    def definition(self):
        return {
            "type": "function",
            "name": "get_calendar_events",
            "description": "Retrieve calendar events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start": {
                        "type": "string",
                        "description": "ISO datetime"
                    },
                    "end": {
                        "type": "string",
                        "description": "ISO datetime"
                    }
                }
            }
        }
    
    def execute(self, **kwargs):

        return self.service.get_events(
            start=kwargs.get("start"),
            end=kwargs.get("end"),
        )