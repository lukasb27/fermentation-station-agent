from typing import Dict
import json
import os
import logging

class ActionLogger():
    """ Class for logging actions the controller has taken. """
    def __init__(self, last_action_file_path: str = "last_known_action.json", log_path: str = "actions.log"):
        """Construct the action logger object, set the logger variable with 
        correct paths for last action fiel and log path. Last action file is used
        to stop excessive logging of the same action.

        :param last_action_file_path: the file to write the last known action to,
          defaults to "last_known_action.json"
        :type last_action_file_path: str, optional
        :param log_path: the file to write the log to, defaults to "actions.log"
        :type log_path: str, optional
        """
        self.last_action_file_path = last_action_file_path
        self.logger = logging.getLogger(__name__)
        self.log_path = log_path
        self.logger.addHandler(logging.FileHandler(log_path))
        self.logger.setLevel(logging.INFO)

    def _check_file_exists(self) -> bool:
        """Check if the last known action file exists already. 
        
        :return: True if file exists.
        :rtype: bool
        """
        return bool(os.path.exists(self.last_action_file_path))

    def get_last_known_action(self) -> Dict[str, str]:
        """Get the last commited action by the fermentation station.

        :return: The last action, either "heating" or "cooling"
        :rtype: Dict[str, str]
        """
        if self._check_file_exists():
            with open(self.last_action_file_path, 'r') as file:
                return json.load(file)
        else:
            return {"last_known_action": "none"}
    
    def set_last_known_action(self, action) -> None:
        """Set the last commited action by the fermentation station.

        :param action: Should be either "heating" or "cooling"
        :type action: str
        """
        with open(self.last_action_file_path, 'w', encoding='utf-8') as f:
            json.dump({"last_known_action": action}, f, ensure_ascii=False, indent=4)
    
    def log_action(self, action) -> None:
        """Read the last known action from the last known action file. 
        If it is different to the current action, write the current action to the log.

        :param action: the action being taken by the controller.
        :type action: str
        """
        if self.get_last_known_action().get("last_known_action") == action:
            return
        else:
            self.logger.info(f"{action} the fermentation station.")