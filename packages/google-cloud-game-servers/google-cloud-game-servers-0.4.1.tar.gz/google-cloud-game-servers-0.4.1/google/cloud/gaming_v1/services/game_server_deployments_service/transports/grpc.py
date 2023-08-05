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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.api_core import gapic_v1  # type: ignore
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.gaming_v1.types import game_server_deployments
from google.longrunning import operations_pb2  # type: ignore
from .base import GameServerDeploymentsServiceTransport, DEFAULT_CLIENT_INFO


class GameServerDeploymentsServiceGrpcTransport(GameServerDeploymentsServiceTransport):
    """gRPC backend transport for GameServerDeploymentsService.

    The game server deployment is used to control the deployment
    of Agones fleets.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "gameservices.googleapis.com",
        credentials: ga_credentials.Credentials = None,
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
            host (Optional[str]):
                 The hostname to connect to.
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
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "gameservices.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
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

        self_signed_jwt_kwargs = cls._get_self_signed_jwt_kwargs(host, scopes)

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            **self_signed_jwt_kwargs,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def list_game_server_deployments(
        self,
    ) -> Callable[
        [game_server_deployments.ListGameServerDeploymentsRequest],
        game_server_deployments.ListGameServerDeploymentsResponse,
    ]:
        r"""Return a callable for the list game server deployments method over gRPC.

        Lists game server deployments in a given project and
        location.

        Returns:
            Callable[[~.ListGameServerDeploymentsRequest],
                    ~.ListGameServerDeploymentsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_game_server_deployments" not in self._stubs:
            self._stubs["list_game_server_deployments"] = self.grpc_channel.unary_unary(
                "/google.cloud.gaming.v1.GameServerDeploymentsService/ListGameServerDeployments",
                request_serializer=game_server_deployments.ListGameServerDeploymentsRequest.serialize,
                response_deserializer=game_server_deployments.ListGameServerDeploymentsResponse.deserialize,
            )
        return self._stubs["list_game_server_deployments"]

    @property
    def get_game_server_deployment(
        self,
    ) -> Callable[
        [game_server_deployments.GetGameServerDeploymentRequest],
        game_server_deployments.GameServerDeployment,
    ]:
        r"""Return a callable for the get game server deployment method over gRPC.

        Gets details of a single game server deployment.

        Returns:
            Callable[[~.GetGameServerDeploymentRequest],
                    ~.GameServerDeployment]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_game_server_deployment" not in self._stubs:
            self._stubs["get_game_server_deployment"] = self.grpc_channel.unary_unary(
                "/google.cloud.gaming.v1.GameServerDeploymentsService/GetGameServerDeployment",
                request_serializer=game_server_deployments.GetGameServerDeploymentRequest.serialize,
                response_deserializer=game_server_deployments.GameServerDeployment.deserialize,
            )
        return self._stubs["get_game_server_deployment"]

    @property
    def create_game_server_deployment(
        self,
    ) -> Callable[
        [game_server_deployments.CreateGameServerDeploymentRequest],
        operations_pb2.Operation,
    ]:
        r"""Return a callable for the create game server deployment method over gRPC.

        Creates a new game server deployment in a given
        project and location.

        Returns:
            Callable[[~.CreateGameServerDeploymentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_game_server_deployment" not in self._stubs:
            self._stubs[
                "create_game_server_deployment"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.gaming.v1.GameServerDeploymentsService/CreateGameServerDeployment",
                request_serializer=game_server_deployments.CreateGameServerDeploymentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_game_server_deployment"]

    @property
    def delete_game_server_deployment(
        self,
    ) -> Callable[
        [game_server_deployments.DeleteGameServerDeploymentRequest],
        operations_pb2.Operation,
    ]:
        r"""Return a callable for the delete game server deployment method over gRPC.

        Deletes a single game server deployment.

        Returns:
            Callable[[~.DeleteGameServerDeploymentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_game_server_deployment" not in self._stubs:
            self._stubs[
                "delete_game_server_deployment"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.gaming.v1.GameServerDeploymentsService/DeleteGameServerDeployment",
                request_serializer=game_server_deployments.DeleteGameServerDeploymentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_game_server_deployment"]

    @property
    def update_game_server_deployment(
        self,
    ) -> Callable[
        [game_server_deployments.UpdateGameServerDeploymentRequest],
        operations_pb2.Operation,
    ]:
        r"""Return a callable for the update game server deployment method over gRPC.

        Patches a game server deployment.

        Returns:
            Callable[[~.UpdateGameServerDeploymentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_game_server_deployment" not in self._stubs:
            self._stubs[
                "update_game_server_deployment"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.gaming.v1.GameServerDeploymentsService/UpdateGameServerDeployment",
                request_serializer=game_server_deployments.UpdateGameServerDeploymentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_game_server_deployment"]

    @property
    def get_game_server_deployment_rollout(
        self,
    ) -> Callable[
        [game_server_deployments.GetGameServerDeploymentRolloutRequest],
        game_server_deployments.GameServerDeploymentRollout,
    ]:
        r"""Return a callable for the get game server deployment
        rollout method over gRPC.

        Gets details a single game server deployment rollout.

        Returns:
            Callable[[~.GetGameServerDeploymentRolloutRequest],
                    ~.GameServerDeploymentRollout]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_game_server_deployment_rollout" not in self._stubs:
            self._stubs[
                "get_game_server_deployment_rollout"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.gaming.v1.GameServerDeploymentsService/GetGameServerDeploymentRollout",
                request_serializer=game_server_deployments.GetGameServerDeploymentRolloutRequest.serialize,
                response_deserializer=game_server_deployments.GameServerDeploymentRollout.deserialize,
            )
        return self._stubs["get_game_server_deployment_rollout"]

    @property
    def update_game_server_deployment_rollout(
        self,
    ) -> Callable[
        [game_server_deployments.UpdateGameServerDeploymentRolloutRequest],
        operations_pb2.Operation,
    ]:
        r"""Return a callable for the update game server deployment
        rollout method over gRPC.

        Patches a single game server deployment rollout. The method will
        not return an error if the update does not affect any existing
        realms. For example - if the default_game_server_config is
        changed but all existing realms use the override, that is valid.
        Similarly, if a non existing realm is explicitly called out in
        game_server_config_overrides field, that will also not result in
        an error.

        Returns:
            Callable[[~.UpdateGameServerDeploymentRolloutRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_game_server_deployment_rollout" not in self._stubs:
            self._stubs[
                "update_game_server_deployment_rollout"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.gaming.v1.GameServerDeploymentsService/UpdateGameServerDeploymentRollout",
                request_serializer=game_server_deployments.UpdateGameServerDeploymentRolloutRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_game_server_deployment_rollout"]

    @property
    def preview_game_server_deployment_rollout(
        self,
    ) -> Callable[
        [game_server_deployments.PreviewGameServerDeploymentRolloutRequest],
        game_server_deployments.PreviewGameServerDeploymentRolloutResponse,
    ]:
        r"""Return a callable for the preview game server deployment
        rollout method over gRPC.

        Previews the game server deployment rollout. This API
        does not mutate the rollout resource.

        Returns:
            Callable[[~.PreviewGameServerDeploymentRolloutRequest],
                    ~.PreviewGameServerDeploymentRolloutResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "preview_game_server_deployment_rollout" not in self._stubs:
            self._stubs[
                "preview_game_server_deployment_rollout"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.gaming.v1.GameServerDeploymentsService/PreviewGameServerDeploymentRollout",
                request_serializer=game_server_deployments.PreviewGameServerDeploymentRolloutRequest.serialize,
                response_deserializer=game_server_deployments.PreviewGameServerDeploymentRolloutResponse.deserialize,
            )
        return self._stubs["preview_game_server_deployment_rollout"]

    @property
    def fetch_deployment_state(
        self,
    ) -> Callable[
        [game_server_deployments.FetchDeploymentStateRequest],
        game_server_deployments.FetchDeploymentStateResponse,
    ]:
        r"""Return a callable for the fetch deployment state method over gRPC.

        Retrieves information about the current state of the
        game server deployment. Gathers all the Agones fleets
        and Agones autoscalers, including fleets running an
        older version of the game server deployment.

        Returns:
            Callable[[~.FetchDeploymentStateRequest],
                    ~.FetchDeploymentStateResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_deployment_state" not in self._stubs:
            self._stubs["fetch_deployment_state"] = self.grpc_channel.unary_unary(
                "/google.cloud.gaming.v1.GameServerDeploymentsService/FetchDeploymentState",
                request_serializer=game_server_deployments.FetchDeploymentStateRequest.serialize,
                response_deserializer=game_server_deployments.FetchDeploymentStateResponse.deserialize,
            )
        return self._stubs["fetch_deployment_state"]


__all__ = ("GameServerDeploymentsServiceGrpcTransport",)
