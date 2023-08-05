# -*- coding: utf-8 -*-
"""Module with configuration classes"""
from abc import abstractmethod
from typing import Any, Callable, Dict, Optional, Type

from everett import NO_VALUE, ConfigurationMissingError  # type: ignore
from everett.manager import ConfigManager, ConfigOSEnv  # type: ignore

_config = ConfigManager([])


class ConfigEnv:
    """Base class for config envs"""

    register = True
    on_top = True

    @abstractmethod
    def get(self, key, namespace=None):
        """abstract method for getting option value"""

    def __init_subclass__(cls: Type['ConfigEnv']):
        if cls.register:
            inst = cls()
            if cls.on_top:
                _config.envs.insert(0, inst)
            else:
                _config.envs.append(inst)


class NamespacedOSEnv(ConfigOSEnv, ConfigEnv):
    """class for env variables"""

    namespace = ''

    def get(self, key, namespace=None):
        return super(NamespacedOSEnv, self).get(key, namespace or self.namespace)


class Param:
    """class for defining parameters"""

    def __init__(
        self,
        namespace=None,
        default=NO_VALUE,  # pylint: disable=too-many-arguments
        alternate_keys=NO_VALUE,
        doc='',
        parser: Callable = str,
        raise_error=True,
        raw_value=False,
    ):  # pylint: disable=too-many-instance-attributes
        self.key = None
        self.namespace = namespace
        self.default = default
        self.alternate_keys = alternate_keys
        self.doc = doc
        self.parser = parser
        self.raise_error = raise_error
        self.raw_value = raw_value

    def __get__(self, instance: Optional['Config'], owner: Type['Config']):
        if instance is None:
            return self
        return _config(
            key=self.key,
            namespace=self.namespace or instance.namespace,
            default=self.default,
            alternate_keys=self.alternate_keys,
            doc=self.doc,
            parser=self.parser,
            raise_error=self.raise_error,
            raw_value=self.raw_value,
        )


class _ConfigMeta(type):
    """Metaclass for Config instances"""

    def __new__(cls, name, bases, namespace):
        for key, value in namespace.items():
            if isinstance(value, Param):
                value.key = key
        meta = super().__new__(cls, name + 'Meta', (cls,) + bases, namespace)
        res = super().__new__(meta, name, bases, {})
        return res


class Config(metaclass=_ConfigMeta):
    """Base class for Configs"""

    namespace: Optional[str] = None

    @classmethod
    def _try__get__(cls, value, default):
        try:
            return value.__get__(cls, type(cls))
        except ConfigurationMissingError:
            return default

    @classmethod
    def get_params(cls) -> Dict[str, Any]:
        """get dict of defined option values"""
        return {
            name: cls._try__get__(value, '--NOT-SET--')
            for name, value in cls.__dict__.items()
            if isinstance(value, Param)
        }

    @classmethod
    def log_params(cls):
        """log option values"""
        from .log import (
            get_logger,
        )  # pylint: disable=import-outside-toplevel, cyclic-import

        logger = get_logger('decleverett')
        logger.info('%s environment:', cls.__name__)
        for name, value in cls.get_params().items():
            logger.info('%s: %s', name, value)


class Core(Config):
    """Core config"""

    DEBUG = Param(default='false', doc='turn debug on', parser=bool)
