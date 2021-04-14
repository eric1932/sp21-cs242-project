from checkin_misc.checkin_class_template import CheckinTemplate, log


class WorkFlow(CheckinTemplate):
    def __init__(self):
        super().__init__("dummy")

    @log
    def exec(self):
        print("dummy work")
        return "success"
