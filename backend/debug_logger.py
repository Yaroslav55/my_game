

class Logger:
    info_header = "Debug info: "
    info_header = "Debug warn: "
    @classmethod
    def info(cls, msg):
        print(f"{cls.info_header}{msg}")

    @classmethod
    def warn(cls, msg):
        print(f"{cls.warn_msg}{msg}")
