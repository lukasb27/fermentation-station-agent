from typing import Dict
import json
import os
import logging

class ActionLogger():
    def __init__(self, last_action_file_path: str = "last_known_action.json", log_path: str = "actions.log"):
        self.last_action_file_path = last_action_file_path
        self.logger = logging.getLogger(__name__)
        self.log_path = log_path
        self.logger.addHandler(logging.FileHandler(log_path))
        self.logger.setLevel(logging.INFO)

    def _check_file_exists(self) -> bool:
        return bool(os.path.exists(self.last_action_file_path))

    def get_last_known_action(self) -> Dict[str, str]:
        if self._check_file_exists():
            with open(self.last_action_file_path, 'r') as file:
                return json.load(file)
        else:
            return {"last_known_action": "none"}
    
    def set_last_known_action(self, action) -> None:
        with open(self.last_action_file_path, 'w', encoding='utf-8') as f:
            json.dump({"last_known_action": action}, f, ensure_ascii=False, indent=4)
    
    def log_action(self, action) -> None:
        if self.get_last_known_action().get("last_known_action") == action:
            return
        else:
            self.logger.info(f"{action} the fermentation station.")