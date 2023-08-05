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
import proto  # type: ignore

from google.protobuf import duration_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1p1beta1",
    manifest={"RunAssetDiscoveryResponse",},
)


class RunAssetDiscoveryResponse(proto.Message):
    r"""Response of asset discovery run
    Attributes:
        state (google.cloud.securitycenter_v1p1beta1.types.RunAssetDiscoveryResponse.State):
            The state of an asset discovery run.
        duration (google.protobuf.duration_pb2.Duration):
            The duration between asset discovery run
            start and end
    """

    class State(proto.Enum):
        r"""The state of an asset discovery run."""
        STATE_UNSPECIFIED = 0
        COMPLETED = 1
        SUPERSEDED = 2
        TERMINATED = 3

    state = proto.Field(proto.ENUM, number=1, enum=State,)
    duration = proto.Field(proto.MESSAGE, number=2, message=duration_pb2.Duration,)


__all__ = tuple(sorted(__protobuf__.manifest))
