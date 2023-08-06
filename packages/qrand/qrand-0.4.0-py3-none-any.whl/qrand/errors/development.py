##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 28, 2021
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

## Copyright 2021 Pedro Rivero
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

from typing import Optional
from warnings import warn


###############################################################################
## RAISE NOT IMPLEMENTED ERROR
###############################################################################
def raise_not_implemented_error(
    subject: str, alt: Optional[str] = None
) -> None:
    """
    Raises NotImplementedError with custom deprecation message.

    Parameters
    ----------
    subject: str
        The non-implemented subject.
    alt: str
        Alternatives.

    Raises
    ------
    NotImplementedError
    """
    MESSAGE = f"{subject} has not been implemented yet."
    if alt:
        MESSAGE += f" Use {alt} instead."
    raise NotImplementedError(MESSAGE)


###############################################################################
## RAISE FUTURE WARNING
###############################################################################
def raise_future_warning(
    subject: str, version: str, alt: Optional[str] = None
) -> None:
    """
    Raises FutureWarning with custom deprecation message.

    Parameters
    ----------
    subject: str
        The subject of future deprecation.
    version: str
        The version in which deprecation will occur.
    alt: str
        Alternatives.

    Raises
    ------
    FutureWarning
    """
    MESSAGE = f"{subject} will be deprecated in version {version}."
    if alt:
        MESSAGE += f" Use {alt} instead."
    warn(MESSAGE, FutureWarning)
