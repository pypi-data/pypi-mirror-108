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

from oceanbolt.com.fleetmanagement_v3.types import service

from .base import FleetManagementServiceTransport, DEFAULT_CLIENT_INFO


class FleetManagementServiceGrpcTransport(FleetManagementServiceTransport):
    """gRPC backend transport for FleetManagementService.

    FleetManagement provides service to manage fleets for clients

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
    def list_fleets(self) -> Callable[
            [service.EmptyParams],
            service.Fleets]:
        r"""Return a callable for the list fleets method over gRPC.

        Lists Fleets for the current user (or fleets that are
        shared with the current user)

        Returns:
            Callable[[~.EmptyParams],
                    ~.Fleets]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_fleets' not in self._stubs:
            self._stubs['list_fleets'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/ListFleets',
                request_serializer=service.EmptyParams.serialize,
                response_deserializer=service.Fleets.deserialize,
            )
        return self._stubs['list_fleets']

    @property
    def create_fleet(self) -> Callable[
            [service.CreateFleetRequest],
            service.Fleet]:
        r"""Return a callable for the create fleet method over gRPC.

        Creates a new Fleet for the current user.

        Returns:
            Callable[[~.CreateFleetRequest],
                    ~.Fleet]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_fleet' not in self._stubs:
            self._stubs['create_fleet'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/CreateFleet',
                request_serializer=service.CreateFleetRequest.serialize,
                response_deserializer=service.Fleet.deserialize,
            )
        return self._stubs['create_fleet']

    @property
    def delete_fleet(self) -> Callable[
            [service.DeleteFleetRequest],
            service.EmptyResponse]:
        r"""Return a callable for the delete fleet method over gRPC.

        Deletes a Fleet for the current user.

        Returns:
            Callable[[~.DeleteFleetRequest],
                    ~.EmptyResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_fleet' not in self._stubs:
            self._stubs['delete_fleet'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/DeleteFleet',
                request_serializer=service.DeleteFleetRequest.serialize,
                response_deserializer=service.EmptyResponse.deserialize,
            )
        return self._stubs['delete_fleet']

    @property
    def describe_fleet(self) -> Callable[
            [service.GetFleetRequest],
            service.Fleet]:
        r"""Return a callable for the describe fleet method over gRPC.

        Retrieves fleet by Fleet id.

        Returns:
            Callable[[~.GetFleetRequest],
                    ~.Fleet]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'describe_fleet' not in self._stubs:
            self._stubs['describe_fleet'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/DescribeFleet',
                request_serializer=service.GetFleetRequest.serialize,
                response_deserializer=service.Fleet.deserialize,
            )
        return self._stubs['describe_fleet']

    @property
    def rename_fleet(self) -> Callable[
            [service.RenameFleetRequest],
            service.Fleet]:
        r"""Return a callable for the rename fleet method over gRPC.

        Changes the name of a Fleet.

        Returns:
            Callable[[~.RenameFleetRequest],
                    ~.Fleet]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'rename_fleet' not in self._stubs:
            self._stubs['rename_fleet'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/RenameFleet',
                request_serializer=service.RenameFleetRequest.serialize,
                response_deserializer=service.Fleet.deserialize,
            )
        return self._stubs['rename_fleet']

    @property
    def share_fleet(self) -> Callable[
            [service.ShareFleetRequest],
            service.Fleet]:
        r"""Return a callable for the share fleet method over gRPC.

        Sets the shared status of the Fleet to be shared.

        Returns:
            Callable[[~.ShareFleetRequest],
                    ~.Fleet]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'share_fleet' not in self._stubs:
            self._stubs['share_fleet'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/ShareFleet',
                request_serializer=service.ShareFleetRequest.serialize,
                response_deserializer=service.Fleet.deserialize,
            )
        return self._stubs['share_fleet']

    @property
    def unshare_fleet(self) -> Callable[
            [service.ShareFleetRequest],
            service.Fleet]:
        r"""Return a callable for the unshare fleet method over gRPC.

        Sets the shared status of the Fleet to be not shared.

        Returns:
            Callable[[~.ShareFleetRequest],
                    ~.Fleet]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'unshare_fleet' not in self._stubs:
            self._stubs['unshare_fleet'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/UnshareFleet',
                request_serializer=service.ShareFleetRequest.serialize,
                response_deserializer=service.Fleet.deserialize,
            )
        return self._stubs['unshare_fleet']

    @property
    def list_vessels(self) -> Callable[
            [service.ListVesselsRequest],
            service.Vessels]:
        r"""Return a callable for the list vessels method over gRPC.

        Retrieves list of vessels in a Fleet.

        Returns:
            Callable[[~.ListVesselsRequest],
                    ~.Vessels]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_vessels' not in self._stubs:
            self._stubs['list_vessels'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/ListVessels',
                request_serializer=service.ListVesselsRequest.serialize,
                response_deserializer=service.Vessels.deserialize,
            )
        return self._stubs['list_vessels']

    @property
    def add_vessel(self) -> Callable[
            [service.AddVesselRequest],
            service.Vessel]:
        r"""Return a callable for the add vessel method over gRPC.

        Adds new vessel to a Fleet. A maximum of 1000 vessels
        can be added to a fleet.

        Returns:
            Callable[[~.AddVesselRequest],
                    ~.Vessel]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'add_vessel' not in self._stubs:
            self._stubs['add_vessel'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/AddVessel',
                request_serializer=service.AddVesselRequest.serialize,
                response_deserializer=service.Vessel.deserialize,
            )
        return self._stubs['add_vessel']

    @property
    def update_vessel(self) -> Callable[
            [service.UpdateVesselRequest],
            service.Vessel]:
        r"""Return a callable for the update vessel method over gRPC.

        Updates existing metadata for a Vessel.

        Returns:
            Callable[[~.UpdateVesselRequest],
                    ~.Vessel]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_vessel' not in self._stubs:
            self._stubs['update_vessel'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/UpdateVessel',
                request_serializer=service.UpdateVesselRequest.serialize,
                response_deserializer=service.Vessel.deserialize,
            )
        return self._stubs['update_vessel']

    @property
    def delete_vessel(self) -> Callable[
            [service.DeleteVesselRequest],
            service.EmptyResponse]:
        r"""Return a callable for the delete vessel method over gRPC.

        Removes a vessel from a Fleet.

        Returns:
            Callable[[~.DeleteVesselRequest],
                    ~.EmptyResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_vessel' not in self._stubs:
            self._stubs['delete_vessel'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/DeleteVessel',
                request_serializer=service.DeleteVesselRequest.serialize,
                response_deserializer=service.EmptyResponse.deserialize,
            )
        return self._stubs['delete_vessel']

    @property
    def batch_add_vessels(self) -> Callable[
            [service.BatchVesselsRequest],
            service.EmptyResponse]:
        r"""Return a callable for the batch add vessels method over gRPC.

        Batch adds vessels into a Fleet. A maximum of 1000
        vessels can be added to a fleet.

        Returns:
            Callable[[~.BatchVesselsRequest],
                    ~.EmptyResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'batch_add_vessels' not in self._stubs:
            self._stubs['batch_add_vessels'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/BatchAddVessels',
                request_serializer=service.BatchVesselsRequest.serialize,
                response_deserializer=service.EmptyResponse.deserialize,
            )
        return self._stubs['batch_add_vessels']

    @property
    def replace_vessels(self) -> Callable[
            [service.BatchVesselsRequest],
            service.EmptyResponse]:
        r"""Return a callable for the replace vessels method over gRPC.

        Replaces the existing vessels in a Fleet with a batch
        of new vessels. This is equivalent to first calling
        DropVessels and then calling BatchAddVessels A maximum
        of 1000 vessels can be added to a fleet.

        Returns:
            Callable[[~.BatchVesselsRequest],
                    ~.EmptyResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'replace_vessels' not in self._stubs:
            self._stubs['replace_vessels'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/ReplaceVessels',
                request_serializer=service.BatchVesselsRequest.serialize,
                response_deserializer=service.EmptyResponse.deserialize,
            )
        return self._stubs['replace_vessels']

    @property
    def drop_vessels(self) -> Callable[
            [service.DropVesselsRequest],
            service.EmptyResponse]:
        r"""Return a callable for the drop vessels method over gRPC.

        Drops all the vessels currently in a fleet.

        Returns:
            Callable[[~.DropVesselsRequest],
                    ~.EmptyResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'drop_vessels' not in self._stubs:
            self._stubs['drop_vessels'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/DropVessels',
                request_serializer=service.DropVesselsRequest.serialize,
                response_deserializer=service.EmptyResponse.deserialize,
            )
        return self._stubs['drop_vessels']

    @property
    def get_fleet_live_map(self) -> Callable[
            [service.GetFleetLiveMapRequest],
            service.GetFleetLiveMapResponse]:
        r"""Return a callable for the get fleet live map method over gRPC.

        GetFleetLiveMap display static location for vessels
        in a fleet (as static image).

        Returns:
            Callable[[~.GetFleetLiveMapRequest],
                    ~.GetFleetLiveMapResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_fleet_live_map' not in self._stubs:
            self._stubs['get_fleet_live_map'] = self.grpc_channel.unary_unary(
                '/oceanbolt.com.fleetmanagement.v3.FleetManagementService/GetFleetLiveMap',
                request_serializer=service.GetFleetLiveMapRequest.serialize,
                response_deserializer=service.GetFleetLiveMapResponse.deserialize,
            )
        return self._stubs['get_fleet_live_map']


__all__ = (
    'FleetManagementServiceGrpcTransport',
)
