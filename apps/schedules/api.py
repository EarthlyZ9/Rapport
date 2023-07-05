from ninja_extra import api_controller, route, ControllerBase

from apps.schedules.services import ScheduleService


@api_controller("/schedules", tags=["Schedule"])
class ScheduleController(ControllerBase):
    def __init__(self, schedule_service: ScheduleService):
        self.service = schedule_service

    @route.get("")
    def list(self, request):
        return "schedules"
