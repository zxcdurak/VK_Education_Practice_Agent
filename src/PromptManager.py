class PromptManager:
    path: str

    def __init__(self, path: str):
        self.path = path

    def get_prompt(self, name: str) -> str:
        try:
            with open(f"{self.path}/{name}" + ".txt") as f:
                return f.read()
        except FileNotFoundError:
            return None


manager = PromptManager(path="prompts/")