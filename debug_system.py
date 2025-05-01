import logging
import sys


class DebugSystem:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise RuntimeError("Use get_instance() instead")

        # Create logger
        self.logger = logging.getLogger('dnd_app')
        self.logger.setLevel(logging.INFO)  # Default level

        # Create handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def set_debug_mode(self, enabled=True):
        """Enable or disable debug mode"""
        if enabled:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def debug(self, message, component=None):
        comp = f"[{component}] " if component else ""
        self.logger.debug(f"{comp}{message}")

    def info(self, message, component=None):
        comp = f"[{component}] " if component else ""
        self.logger.info(f"{comp}{message}")