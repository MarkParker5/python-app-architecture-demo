from coordinator import Coordinator


def run(): # entry point, no logic here, only run the coordinator
    coordinator = Coordinator()
    coordinator.setup_initial_state()

if __name__ == '__main__':
    run()
