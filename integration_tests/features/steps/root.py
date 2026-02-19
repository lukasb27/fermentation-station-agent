from behave import when, then
import requests 

@when('we curl the {location} of the web app')
def step_when_switch_blender_on(context, location):
    location_map = {'root': ''}
    context.response = requests.get(f'http://localhost:8000/{location_map[location]}')

@then('it should return {status_code} status code')
def step_then_should_transform_into(context, status_code):
    assert str(context.response.status_code) == '200' 