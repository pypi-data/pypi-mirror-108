##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 29, 2021
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

from typing import Callable, List, Optional

from qiskit import BasicAer
from qiskit.providers import BackendV1 as Backend
from qiskit.providers import Provider
from qiskit.providers.ibmq import IBMQError, least_busy
from qiskit.providers.models import BackendConfiguration

from ...helpers import validate_type
from ...protocols import ProtocolResult, QuantumProtocol
from ..platform import QuantumPlatform
from .backend import QiskitBackend
from .circuit import QiskitCircuit
from .job import QiskitJob

###############################################################################
## CUSTOM TYPES
###############################################################################
BackendFilter = Callable[[Backend], bool]


###############################################################################
## QISKIT PLATFORM
###############################################################################
class QiskitPlatform(QuantumPlatform):
    def __init__(
        self,
        provider: Optional[Provider] = None,
        backend: Optional[Backend] = None,
        backend_filter: Optional[BackendFilter] = None,
    ) -> None:
        if backend:
            provider = None
        elif provider:
            backend = self._get_best_backend(
                provider=provider,
                backend_filter=backend_filter,
            )
        else:
            backend = BasicAer.get_backend("qasm_simulator")
        self.provider: Optional[Provider] = provider
        self.backend: Backend = backend
        self.backend_filter: Optional[BackendFilter] = backend_filter

    ############################### PUBLIC API ###############################
    @property
    def backend(self) -> Backend:
        return self._backend

    @backend.setter
    def backend(self, backend: Backend) -> None:
        validate_type(backend, Backend)
        self._backend: Backend = backend

    @property
    def backend_filter(self) -> Optional[BackendFilter]:
        return self._backend_filter or self.default_backend_filter

    @backend_filter.setter
    def backend_filter(self, backend_filter: Optional[BackendFilter]) -> None:
        try:
            assert callable(backend_filter)
            assert isinstance(backend_filter(self.backend), bool)
            self._backend_filter: Optional[BackendFilter] = backend_filter
        except Exception:
            self._backend_filter = None

    @property
    def provider(self) -> Optional[Provider]:
        return self._provider

    @provider.setter
    def provider(self, provider: Optional[Provider]) -> None:
        validate_type(provider, (Provider, type(None)))
        self._provider: Provider = provider

    @staticmethod
    def default_backend_filter(b: Backend) -> bool:
        config: BackendConfiguration = b.configuration()
        return config.memory and not config.simulator

    def create_circuit(self, num_qubits: int) -> QiskitCircuit:
        return QiskitCircuit(num_qubits)

    def create_job(  # type: ignore
        self,
        circuit: QiskitCircuit,
        backend: QiskitBackend,
        num_measurements: Optional[int],
    ) -> QiskitJob:
        return QiskitJob(circuit, backend, num_measurements)

    def fetch_random_bits(self, protocol: QuantumProtocol) -> str:
        validate_type(protocol, QuantumProtocol)
        result: ProtocolResult = protocol.run(self)
        return result.bitstring

    def retrieve_backend(self) -> QiskitBackend:
        if self.provider:
            self.backend = self._get_best_backend(
                provider=self.provider,
                backend_filter=self.backend_filter,
            )
        return QiskitBackend(self.backend)

    ############################### PRIVATE API ###############################
    @classmethod
    def _get_best_backend(
        cls,
        provider: Provider,
        backend_filter: Optional[BackendFilter] = None,
    ) -> Backend:
        if not backend_filter:
            backend_filter = cls.default_backend_filter
        backends: List[Backend] = provider.backends(filters=backend_filter)
        if not backends:
            raise IBMQError(  # TODO
                "No backends matching the filtering critera on the \
                requested provider."
            )
        return least_busy(backends)
