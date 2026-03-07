Feature: Testing root of fermentation station agent

    Scenario Outline: curl root of fermentation station
        When we curl the <location> of the web app
        Then it should return <status code> status code

        Examples: Web app paths
            | location | status code |
            | root     | 200         |
