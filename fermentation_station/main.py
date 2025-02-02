from fermentation-station.models.controller import Controller 

def main():
    controller = Controller()
    print(controller.perform_action())

if __name__ == "__main__":
    main()