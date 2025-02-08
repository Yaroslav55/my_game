

class Logger:
    info_header = "Debug info: "
    warn_header = "Debug warn: "
    err_header = "Debug warn: "
    @classmethod
    def info(cls, msg):
        print(f"{cls.info_header}{msg}")

    @classmethod
    def warn(cls, msg):
        print(f"{cls.warn_header}{msg}")

    @classmethod
    def err(cls, msg):
        print(f"{cls.err_header}{msg}")
