from typing import Union


class TaskID:
    def __init__(self, username: str, template: str, num: Union[int, str]):
        self.username = username
        self.template = template
        self.num = str(num)
        self.as_str = f"{self.username}-{self.template}-{self.num}"

    def __str__(self):
        return self.as_str
