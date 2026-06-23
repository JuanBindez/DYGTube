
import logging

class DebugInfo:
    logging.basicConfig(filename="DYGTUbe_Debug_info.log",
                        level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')
    logger_info = logging.getLogger("DYGTUbe_Debug_info")

    logging.basicConfig(filename='DYGTUbe_Error.log',
                        level=logging.ERROR,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')
    
    logger_error = logging.getLogger("DYGTUbe_error")


    info = logger_info.info("------------------------------[START DEBUG]--------------------------------")

