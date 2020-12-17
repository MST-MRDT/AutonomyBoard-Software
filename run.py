import argparse
import logging
import logging.config
import yaml
import core
import interfaces
#import vision
import importlib
import os
import sys
import time 


def setup_logger(level) -> logging.Logger:
    '''
    Sets up the logger used in the autonomy project with appropriate
    handlers and formatting

    Returns
    -------

        Logger: root set up for console and file logging
    '''

    # logging file
    yaml_conf = yaml.safe_load(open('core/logging.yaml', 'r').read())
    logging.config.dictConfig(yaml_conf)

    for handler in logging.getLogger().handlers:
        if isinstance(handler, type(logging.StreamHandler())):
            handler.setLevel(level)

    return logging.getLogger()


def main() -> None:
    parser = argparse.ArgumentParser()

    # Maps the passed in file name to a known module and main() (if it is known)
    parser.add_argument('--file', help="Specify the name of the custom module to be run", default="autonomy.py")

    # Optional parameter to set logging level
    parser.add_argument('--level', choices=["DEBUG", "INFO", "WARN", "CRITICAL", "ERROR"], default="INFO")

    args = parser.parse_args()
    if (level := getattr(logging, args.level, -1)) < 0:
        parser.print_help()
        exit(1)

    # Add the examples folder to our path so we can run example files
    sys.path.insert(0, 'example/')

    # Setup the logger, also pass-in optional logging level for console output
    logger = setup_logger(level)

    # Initialize the rovecomm node
    core.rovecomm_node = core.RoveComm(11000, ('127.0.0.1', 11111))

    # Initialize the state machine
    core.states.state_machine = core.states.StateMachine()

    # Initialize the ZED handler
    # vision.camera_handler = vision.ZedHandler()
    # vision.camera_handler.start()

    # Initialize the Interfaces
    interfaces.drive_board = interfaces.DriveBoard()
    interfaces.nav_board = interfaces.NavBoard()

    # Sleep so everything can be set up
    time.sleep(1)

    try:
        # Remove .py and directly import module
        module = importlib.import_module(os.path.splitext(args.file)[0])
        module.main()
    except ImportError as error:
        # Couldn't find module because file doesn't exist or tried to import
        # from package
        logger.error(f"Failed to import module '{args.file}'")
        logger.error(error)
        core.rovecomm_node.close_thread()
        # vision.camera_handler.close()
        exit(1)
    except NameError as error:
        # Successful import but module does not define main
        logger.error(f"{args.file}: Undefined reference to main")
        logger.error(error)
        core.rovecomm_node.close_thread()
        # vision.camera_handler.close()
        exit(1)
    else:
        core.rovecomm_node.close_thread()
        # vision.camera_handler.close()
        exit(0)

if __name__ == "__main__":
    # Run main()
    main()
