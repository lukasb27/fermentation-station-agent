import pytest
from src.models.last_known_action import LastKnownAction
import json 
import os

FILE_PATH = "test_last_known_action.json"

@pytest.fixture()
def last_known_action_file():
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump({"last_known_action": "heating"}, f, ensure_ascii=False, indent=4)
    yield
    # os.remove(FILE_PATH)

@pytest.fixture()
def last_known_action():
    yield LastKnownAction(file_path=FILE_PATH)

def test_reading_last_known_action(last_known_action_file, last_known_action):
    last_known_action_file
    assert last_known_action.get_last_known_action() == {"last_known_action": "heating"}

def test_setting_list_known_action(last_known_action):
    last_known_action.set_last_known_action("cooling")
    with open(FILE_PATH, 'r') as file:
        data = json.load(file)

    assert data == {"last_known_action": "cooling"}
    os.remove(FILE_PATH)

def test_file_exists_fails(last_known_action):
    last_known_action.file_path = "will_never_exist.json"
    assert last_known_action._check_file_exists() == False

def test_file_exists_succeeds(last_known_action):
    file_path = "will_exist.json"
    last_known_action.file_path = file_path
    open(file_path, "a").close()
    assert last_known_action._check_file_exists() == True
    os.remove(file_path)
    
     