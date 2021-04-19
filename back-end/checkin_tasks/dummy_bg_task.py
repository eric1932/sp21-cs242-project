from checkin_misc.checkin_class_template import CheckinTemplate, log


class Workflow(CheckinTemplate):
    def __init__(self):
        super().__init__("dummy")

    @log
    def exec(self):
        print("---")
        print("dummy work execution")
        print("---")
        return "success"
