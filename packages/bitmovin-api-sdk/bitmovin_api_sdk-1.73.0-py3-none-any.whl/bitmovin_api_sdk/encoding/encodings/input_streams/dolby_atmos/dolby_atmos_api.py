# coding: utf-8

from __future__ import absolute_import

from bitmovin_api_sdk.common import BaseApi, BitmovinApiLoggerBase
from bitmovin_api_sdk.common.poscheck import poscheck_except
from bitmovin_api_sdk.models.bitmovin_response import BitmovinResponse
from bitmovin_api_sdk.models.dolby_atmos_ingest_input_stream import DolbyAtmosIngestInputStream
from bitmovin_api_sdk.models.response_envelope import ResponseEnvelope
from bitmovin_api_sdk.models.response_error import ResponseError
from bitmovin_api_sdk.encoding.encodings.input_streams.dolby_atmos.dolby_atmos_ingest_input_stream_list_query_params import DolbyAtmosIngestInputStreamListQueryParams


class DolbyAtmosApi(BaseApi):
    @poscheck_except(2)
    def __init__(self, api_key, tenant_org_id=None, base_url=None, logger=None):
        # type: (str, str, str, BitmovinApiLoggerBase) -> None

        super(DolbyAtmosApi, self).__init__(
            api_key=api_key,
            tenant_org_id=tenant_org_id,
            base_url=base_url,
            logger=logger
        )

    def create(self, encoding_id, dolby_atmos_ingest_input_stream, **kwargs):
        # type: (string_types, DolbyAtmosIngestInputStream, dict) -> DolbyAtmosIngestInputStream
        """Add Dolby Atmos input stream

        :param encoding_id: Id of the encoding
        :type encoding_id: string_types, required
        :param dolby_atmos_ingest_input_stream: The Dolby Atmos input stream to be created
        :type dolby_atmos_ingest_input_stream: DolbyAtmosIngestInputStream, required
        :return: Dolby Atmos input stream
        :rtype: DolbyAtmosIngestInputStream
        """

        return self.api_client.post(
            '/encoding/encodings/{encoding_id}/input-streams/dolby-atmos',
            dolby_atmos_ingest_input_stream,
            path_params={'encoding_id': encoding_id},
            type=DolbyAtmosIngestInputStream,
            **kwargs
        )

    def delete(self, encoding_id, input_stream_id, **kwargs):
        # type: (string_types, string_types, dict) -> BitmovinResponse
        """Delete Dolby Atmos input stream

        :param encoding_id: Id of the encoding
        :type encoding_id: string_types, required
        :param input_stream_id: Id of the Dolby Atmos input stream
        :type input_stream_id: string_types, required
        :return: Id of the Dolby Atmos input stream
        :rtype: BitmovinResponse
        """

        return self.api_client.delete(
            '/encoding/encodings/{encoding_id}/input-streams/dolby-atmos/{input_stream_id}',
            path_params={'encoding_id': encoding_id, 'input_stream_id': input_stream_id},
            type=BitmovinResponse,
            **kwargs
        )

    def get(self, encoding_id, input_stream_id, **kwargs):
        # type: (string_types, string_types, dict) -> DolbyAtmosIngestInputStream
        """Dolby Atmos input stream details

        :param encoding_id: Id of the encoding
        :type encoding_id: string_types, required
        :param input_stream_id: Id of the Dolby Atmos input stream
        :type input_stream_id: string_types, required
        :return: Dolby Atmos Input Stream
        :rtype: DolbyAtmosIngestInputStream
        """

        return self.api_client.get(
            '/encoding/encodings/{encoding_id}/input-streams/dolby-atmos/{input_stream_id}',
            path_params={'encoding_id': encoding_id, 'input_stream_id': input_stream_id},
            type=DolbyAtmosIngestInputStream,
            **kwargs
        )

    def list(self, encoding_id, query_params=None, **kwargs):
        # type: (string_types, DolbyAtmosIngestInputStreamListQueryParams, dict) -> DolbyAtmosIngestInputStream
        """List Dolby Atmos input streams

        :param encoding_id: Id of the encoding
        :type encoding_id: string_types, required
        :param query_params: Query parameters
        :type query_params: DolbyAtmosIngestInputStreamListQueryParams
        :return: List Dolby Atmos input streams
        :rtype: DolbyAtmosIngestInputStream
        """

        return self.api_client.get(
            '/encoding/encodings/{encoding_id}/input-streams/dolby-atmos',
            path_params={'encoding_id': encoding_id},
            query_params=query_params,
            pagination_response=True,
            type=DolbyAtmosIngestInputStream,
            **kwargs
        )
