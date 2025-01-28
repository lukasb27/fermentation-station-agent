import pytest
from src.models.action_logger import ActionLogger
import json 
import os

last_action_file_path = "test_last_known_action.json"

@pytest.fixture()
def last_known_action_file():
    with open(last_action_file_path, 'w', encoding='utf-8') as f:
            json.dump({"last_known_action": "heating"}, f, ensure_ascii=False, indent=4)
    yield
    os.remove(last_action_file_path)

@pytest.fixture()
def last_known_action():
    yield ActionLogger(last_action_file_path=last_action_file_path, log_path="testing.log")

def test_reading_last_known_action(last_known_action_file, last_known_action):
    last_known_action_file
    assert last_known_action.get_last_known_action() == {"last_known_action": "heating"}

def test_setting_list_known_action(last_known_action):
    last_known_action.set_last_known_action("cooling")
    with open(last_action_file_path, 'r') as file:
        data = json.load(file)

    assert data == {"last_known_action": "cooling"}
    os.remove(last_action_file_path)

def test_file_exists_fails(last_known_action):
    last_known_action.last_action_file_path = "will_never_exist.json"
    assert last_known_action._check_file_exists() == False

def test_file_exists_succeeds(last_known_action):
    last_action_file_path = "will_exist.json"
    last_known_action.last_action_file_path = last_action_file_path
    open(last_action_file_path, "a").close()
    assert last_known_action._check_file_exists() == True
    os.remove(last_action_file_path)
    
def test_writing_log(last_known_action_file, last_known_action):
    last_known_action.log_action("cooling")
    assert bool(os.path.exists(last_known_action.log_path))
    assert os.path.getsize(last_known_action.log_path) > 0
    os.remove(last_known_action.log_path)