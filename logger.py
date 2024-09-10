import logging
import os

class logger_class:
    def __init__(self, full_path, file_name):

        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(logging.DEBUG)

        self.logger.debug(f"File path: {full_path}")
        
        # Ensure the result directory exists
        result_dir = os.path.join(os.path.dirname(__file__), f"output/{file_name}")
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        handler = logging.FileHandler(filename=f"output/{file_name}/{file_name}.log", mode='w')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def get(self):
        return self.logger