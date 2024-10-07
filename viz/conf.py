import os
from typing import Any, Dict, Mapping


class Conf:
    """
        Configurator class

    This class is used to configure the application. It takes a dictionary of default values
    and allows the user to override these values with environment variables.

    Parameters:
    default_values (Dict[str, Any]): A dictionary of default configuration values.
    environ (Mapping[str, str], optional): A dictionary of environment variables. Defaults to os.environ.
    **kwargs: Additional keyword arguments to override default values.

    Attributes:
    default_values (Dict[str, Any]): The dictionary of default configuration values.

    Example:
    >>> conf = Conf({'debug': False, 'timeout': 10})
    >>> print(conf.debug)  # prints False
    >>> print(conf.timeout)  # prints 10

    # override with environment variables
    >>> os.environ['CONF_DEBUG'] = 'True'
    >>> os.environ['CONF_TIMEOUT'] = '20'
    >>> conf = Conf({'debug': False, 'timeout': 10})
    >>> print(conf.debug)  # prints True
    >>> print(conf.timeout)  # prints 20

    # inject with environment variables
    >>> conf = Conf({'debug': False, 'timeout': 10},
    >>>               environ={"CONF_DEBUG": "False","CONF_TIMEOUT": "20"})
    >>> print(conf.debug)  # prints True
    >>> print(conf.timeout)  # prints 20
    """

    def __init__(
        self,
        default_values: Dict[str, Any],
        environ: Mapping[
            str, str
        ] = os.environ,  # use Mapping to be compatible with os.environ
        **kwargs: Any,
    ):
        if not default_values:
            raise ValueError("default_values is mandatory")

        self.default_values: Dict[str, Any] = default_values

        for key, value in default_values.items():
            env_key = f"CONF_{key.upper()}"
            if key in kwargs:
                setattr(self, key, type(value)(kwargs[key]))
                continue

            if env_key in environ:
                setattr(self, key, type(value)(environ[env_key]))
                continue

            setattr(self, key, value)
