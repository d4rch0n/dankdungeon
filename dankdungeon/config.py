import yaml

from . import util


class Config(dict):
    DEFAULTS = {}

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        for key, default in cls.DEFAULTS.items():
            data[key] = data.get(key, default)
        conf = cls(**data)
        if 'names' in data:
            race_names = util.race_dict(data['names'])
            conf.name_gen = util.make_race_name_gen(race_names)
        if 'race_freq' in data:
            conf.rand_race = util.race_freq_gen(data['race_freq'])
        return conf
