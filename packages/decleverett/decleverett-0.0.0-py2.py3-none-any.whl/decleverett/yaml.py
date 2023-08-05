# -*- coding: utf-8 -*-
import yaml
from everett.ext.yamlfile import ConfigYamlEnv

from .base import ConfigEnv


def add_yaml_source(path, top=True):
    class _YamlEnv(ConfigYamlEnv, ConfigEnv):
        on_top = top

        def __init__(self):
            super().__init__(path)

        def parse_yaml_file(self, path):
            """Parse yaml file at ``path`` and return a dict."""
            with open(path, 'r') as fp:
                data = yaml.safe_load(fp)

            if not data:
                return {}

            return {
                f'{ns}_{name}'.upper(): value
                for ns, values in data.items()
                for name, value in values.items()
            }

    return _YamlEnv
