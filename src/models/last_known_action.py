from typing import Dict
import json
import os

class LastKnownAction():
    def __init__(self, file_path: str = "last_known_action.json"):
        self.file_path = file_path

    def _check_file_exists(self) -> bool:
        return bool(os.path.exists(self.file_path))

    def get_last_known_action(self) -> Dict[str, str]:
        if self._check_file_exists():
            with open(self.file_path, 'r') as file:
                return json.load(file)
        else:
            return {"last_known_action": "none"}
    
    def set_last_known_action(self, action) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump({"last_known_action": action}, f, ensure_ascii=False, indent=4)