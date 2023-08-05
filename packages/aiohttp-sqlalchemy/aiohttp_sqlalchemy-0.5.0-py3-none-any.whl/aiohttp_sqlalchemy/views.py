from abc import ABCMeta
from aiohttp.abc import AbstractView
from aiohttp.web import View
from typing import TYPE_CHECKING
import warnings

from aiohttp_sqlalchemy.constants import DEFAULT_KEY

if TYPE_CHECKING:
    from aiohttp.web import Request
    from sqlalchemy.ext.asyncio import AsyncSession
    from typing import Any


class SAViewMixin:
    """ SQLAlchemy class based view mixin. """
    request: 'Request'

    def __init__(self):
        msg = "SAViewMixin is deprecated. Use SAAbstractView."
        warnings.warn(msg, DeprecationWarning, stacklevel=2)

    @property
    def sa_main_session(self) -> 'AsyncSession':
        msg = "SAViewMixin.sa_main_session is deprecated. " \
              "Use SAViewMixin.sa_session()."
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        return self.request[DEFAULT_KEY]

    def sa_session(self, key: str = DEFAULT_KEY) -> 'AsyncSession':
        return self.request[key]


class SAAbstractView(AbstractView, metaclass=ABCMeta):
    """ SQLAlchemy view based on aiohttp.abc.AbstractView """

    @property
    def sa_main_session(self) -> 'AsyncSession':
        msg = "SAAbstractView.sa_main_session is deprecated. " \
              "Use SAAbstractView.sa_session()."
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        return self.request[DEFAULT_KEY]

    def sa_session(self, key: str = DEFAULT_KEY) -> 'AsyncSession':
        return self.request[key]


class SAOneModelMixin(SAAbstractView, metaclass=ABCMeta):
    sa_model: 'Any'  # Not all developers use declarative mapping


class SABaseView(View, SAAbstractView):
    """ Simple SQLAlchemy view based on aiohttp.web.View """


class SAView(View, SAOneModelMixin):
    """ One model SQLAlchemy view """
