import yaml


class Config(dict):
    DEFAULTS = {}

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        for key, default in cls.DEFAULTS.items():
            data[key] = data.get(key, default)
        return cls(**data)
