# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers   # type: ignore
from google.api_core import gapic_v1       # type: ignore
from google import auth                    # type: ignore
from google.auth import credentials        # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from oceanbolt.com.tonnage_v3.types import service

from .base import TonnageServiceTransport, DEFAULT_CLIENT_INFO


class TonnageServiceGrpcTransport(TonnageServiceTransport):
    """gRPC backend transport for TonnageService.

    TonnageService provides am API service to get tonnage data

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """
    _stubs: Dict[str, Callable]

    def __init__(self, *,
            host: str = 'api.oceanbolt.com',
            credentials: credentials.Credentials = None,
            credentials_file: str = None,
            scopes: Sequence[str] = None,
            channel: grpc.Channel = None,
            api_mtls_endpoint: str = None,
            client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
            ssl_channel_credentials: grpc.ChannelCredentials = None,
            client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._ssl_channel_credentials = ssl_channel_credentials

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        elif api_mtls_endpoint:
            host = api_mtls_endpoint if ":" in api_mtls_endpoint else api_mtls_endpoint + ":443"

            if credentials is None:
                credentials, _ = auth.default(scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id)

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            self._ssl_channel_credentials = ssl_credentials
        else:
            host = host if ":" in host else host + ":443"

            if credentials is None:
                credentials, _ = auth.default(scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id)

            if client_cert_source_for_mtls and not ssl_channel_credentials:
                cert, key = client_cert_source_for_mtls()
                self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=self._ssl_channel_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._stubs = {}  # type: Dict[str, Callable]

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

    @classmethod
    def create_channel(cls,
                       host: str = 'api.oceanbolt.com',
                       credentials: credentials.Credentials = None,
                       credentials_file: str = None,
                       scopes: Optional[Sequence[str]] = None,
                       quota_project_id: Optional[str] = None,
                       **kwargs) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def get_tonnage_zone_count(self) -> Callable[
            [service.GetTonnageDataRequest],
            service.GetTonnageZoneCountResponse]:
        r"""Return a callable for the get tonnage zone count method over gRPC.

        Fetches tonnage counts timeseries.

        Returns:
            Callable[[~.GetTonnageDataRequest],
                    ~.GetTonnageZoneCountResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_tonnage_zone_count' not in self._stubs:
            self._stubs['get_tonnage_zone_count'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.tonnage.v3.TonnageService/GetTonnageZoneCount',
                request_serializer=service.GetTonnageDataRequest.serialize,
                response_deserializer=service.GetTonnageZoneCountResponse.deserialize,
            )
        return self._stubs['get_tonnage_zone_count']

    @property
    def get_tonnage_fleet_speed(self) -> Callable[
            [service.GetTonnageDataRequest],
            service.GetFleetSpeedResponse]:
        r"""Return a callable for the get tonnage fleet speed method over gRPC.

        Fetches fleet speed timeseries.

        Returns:
            Callable[[~.GetTonnageDataRequest],
                    ~.GetFleetSpeedResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_tonnage_fleet_speed' not in self._stubs:
            self._stubs['get_tonnage_fleet_speed'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.tonnage.v3.TonnageService/GetTonnageFleetSpeed',
                request_serializer=service.GetTonnageDataRequest.serialize,
                response_deserializer=service.GetFleetSpeedResponse.deserialize,
            )
        return self._stubs['get_tonnage_fleet_speed']

    @property
    def get_global_tonnage_status(self) -> Callable[
            [service.GetGlobalTonnageStatusRequest],
            service.GetGlobalTonnageStatusResponse]:
        r"""Return a callable for the get global tonnage status method over gRPC.

        Fetches global tonnage status timeseries.

        Returns:
            Callable[[~.GetGlobalTonnageStatusRequest],
                    ~.GetGlobalTonnageStatusResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_global_tonnage_status' not in self._stubs:
            self._stubs['get_global_tonnage_status'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.tonnage.v3.TonnageService/GetGlobalTonnageStatus',
                request_serializer=service.GetGlobalTonnageStatusRequest.serialize,
                response_deserializer=service.GetGlobalTonnageStatusResponse.deserialize,
            )
        return self._stubs['get_global_tonnage_status']

    @property
    def get_tonnage_fleet_status(self) -> Callable[
            [service.GetTonnageFleetRequest],
            service.GetTonnageFleetStatusResponse]:
        r"""Return a callable for the get tonnage fleet status method over gRPC.

        Provides fleet status timeseries of how the fleet
        have developed over time. This timeseries shows number
        of active vessels on the water at any given time.

        Returns:
            Callable[[~.GetTonnageFleetRequest],
                    ~.GetTonnageFleetStatusResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_tonnage_fleet_status' not in self._stubs:
            self._stubs['get_tonnage_fleet_status'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.tonnage.v3.TonnageService/GetTonnageFleetStatus',
                request_serializer=service.GetTonnageFleetRequest.serialize,
                response_deserializer=service.GetTonnageFleetStatusResponse.deserialize,
            )
        return self._stubs['get_tonnage_fleet_status']

    @property
    def get_tonnage_fleet_growth(self) -> Callable[
            [service.GetTonnageFleetRequest],
            service.GetTonnageFleetGrowthResponse]:
        r"""Return a callable for the get tonnage fleet growth method over gRPC.

        Provides fleet growth timeseries of how the fleet
        have developed over time. This timeseries shows number
        of vessels added to/removed from the fleet during any
        given period.

        Returns:
            Callable[[~.GetTonnageFleetRequest],
                    ~.GetTonnageFleetGrowthResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_tonnage_fleet_growth' not in self._stubs:
            self._stubs['get_tonnage_fleet_growth'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.tonnage.v3.TonnageService/GetTonnageFleetGrowth',
                request_serializer=service.GetTonnageFleetRequest.serialize,
                response_deserializer=service.GetTonnageFleetGrowthResponse.deserialize,
            )
        return self._stubs['get_tonnage_fleet_growth']

    @property
    def get_tonnage_chinese_waters(self) -> Callable[
            [service.TonnageChineseWatersRequest],
            service.TonnageChineseWatersResponse]:
        r"""Return a callable for the get tonnage chinese waters method over gRPC.

        Provides chinese waters tonnage timeseries data. This
        timeseries shows the number of Chinese flagged that are
        trading inside and outside of Chinese waters
        respectively.

        Returns:
            Callable[[~.TonnageChineseWatersRequest],
                    ~.TonnageChineseWatersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_tonnage_chinese_waters' not in self._stubs:
            self._stubs['get_tonnage_chinese_waters'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.tonnage.v3.TonnageService/GetTonnageChineseWaters',
                request_serializer=service.TonnageChineseWatersRequest.serialize,
                response_deserializer=service.TonnageChineseWatersResponse.deserialize,
            )
        return self._stubs['get_tonnage_chinese_waters']

    @property
    def get_tonnage_zone_changes(self) -> Callable[
            [service.GetTonnageZoneChangesRequest],
            service.GetTonnageZoneChangesResponse]:
        r"""Return a callable for the get tonnage zone changes method over gRPC.

        Provides timeseries data on the number of vessels
        that cross zone boundaries during any given period.

        Returns:
            Callable[[~.GetTonnageZoneChangesRequest],
                    ~.GetTonnageZoneChangesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_tonnage_zone_changes' not in self._stubs:
            self._stubs['get_tonnage_zone_changes'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.tonnage.v3.TonnageService/GetTonnageZoneChanges',
                request_serializer=service.GetTonnageZoneChangesRequest.serialize,
                response_deserializer=service.GetTonnageZoneChangesResponse.deserialize,
            )
        return self._stubs['get_tonnage_zone_changes']


__all__ = (
    'TonnageServiceGrpcTransport',
)
