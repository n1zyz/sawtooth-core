# Copyright 2017 Intel Corporation
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
# ------------------------------------------------------------------------------

import json
from aiohttp.web import HTTPError


class _ApiError(HTTPError):
    """A parent class for all REST API errors. Extends aiohttp's HTTPError,
    so instances will be caught automatically be the API, and turned into a
    response to send back to clients. Children should not define any methods,
    just four class variables which the parent __init__ will reference.

    Attributes:
        api_code (int): The fixed code to include in the JSON error response.
            Once established, this code should never change.
        status_code (int): HTTP status to use. Referenced withinin HTTPError's
            __init__ method.
        title (str): A short headline for the error.
        message (str): The human-readable description of the error.

    Raises:
        AssertionError: If api_code, status_code, title, or message were
            not set.
    """
    api_code = None
    status_code = None
    title = None
    message = None

    def __init__(self):
        assert self.api_code is not None, 'Invalid ApiError, api_code not set'
        assert self.status_code is not None, 'Invalid ApiError, status not set'
        assert self.title is not None, 'Invalid ApiError, title not set'
        assert self.message is not None, 'Invalid ApiError, message not set'

        error = {
            'code': self.api_code,
            'title': self.title,
            'message': self.message}

        super().__init__(
            content_type='application/json',
            text=json.dumps(
                {'error': error},
                indent=2,
                separators=(',', ': '),
                sort_keys=True))


class UnknownValidatorError(_ApiError):
    api_code = 10
    status_code = 500
    title = 'Unknown Validator Error'
    message = ('An unknown error occurred with the validator while '
               'processing your request.')


class ValidatorNotReady(_ApiError):
    api_code = 15
    status_code = 503
    title = 'Validator Not Ready'
    message = ('The validator has no genesis block, and is not yet ready to '
               'be queried. Try your request again later.')


class ValidatorTimedOut(_ApiError):
    api_code = 17
    status_code = 503
    title = 'Validator Timed Out'
    message = ('The request timed out while waiting for a response from the '
               'validator. Your request may or may not have been processed.')


class ValidatorDisconnected(_ApiError):
    api_code = 18
    status_code = 503
    title = 'Validator Disconnected'
    message = ('The validator disconnected before sending a response. '
               'Try your request again later.')


class ResourceHeaderInvalid(_ApiError):
    api_code = 21
    status_code = 500
    title = 'Invalid Resource Header'
    message = ('The resource fetched from the validator had an invalid '
               'header, and may be corrupted.')


class StatusResponseMissing(_ApiError):
    api_code = 27
    status_code = 500
    title = 'Unable to Fetch Statuses'
    message = ('An unknown error occurred while attempting to fetch batch '
               'statuses, and nothing was returned.')


class SubmittedBatchesInvalid(_ApiError):
    api_code = 30
    status_code = 400
    title = 'Submitted Batches Invalid'
    message = ('The submitted BatchList was rejected by the validator. It was '
               'poorly formed, or has an invalid signature.')


class NoBatchesSubmitted(_ApiError):
    api_code = 34
    status_code = 400
    title = 'No Batches Submitted'
    message = ('The protobuf BatchList you submitted was empty and contained '
               'no Batches. You must submit at least one Batch.')


class BadProtobufSubmitted(_ApiError):
    api_code = 35
    status_code = 400
    title = 'Protobuf Not Decodable'
    message = ('The protobuf BatchList you submitted was malformed and could '
               'not be read.')


class SubmissionWrongContentType(_ApiError):
    api_code = 42
    status_code = 400
    title = 'Wrong Content Type'
    message = ("Batches must be submitted in a BatchList protobuf binary, "
               "with a 'Content-Type' header of 'application/octet-stream'.")


class StatusWrongContentType(_ApiError):
    api_code = 43
    status_code = 400
    title = 'Wrong Content Type'
    message = ("Requests for batch statuses sent as a POST must have a "
               "'Content-Type' header of 'application/json'.")


class StatusBodyInvalid(_ApiError):
    api_code = 46
    status_code = 400
    title = 'Bad Status Request'
    message = ('Requests for batch statuses sent as a POST must have a JSON '
               'formatted body with an array of at least one id string.')


class HeadNotFound(_ApiError):
    api_code = 50
    status_code = 404
    title = 'Head Not Found'
    message = ("There is no block with the id specified in the 'head' "
               "query parameter.")


class CountInvalid(_ApiError):
    api_code = 53
    status_code = 400
    title = 'Invalid Count Query'
    message = ("The 'count' query parameter must be a positive, "
               "non-zero integer.")


class PagingInvalid(_ApiError):
    api_code = 54
    status_code = 400
    title = 'Invalid Paging Query'
    message = ("Paging request failed as written. One or more of the "
               "'min', 'max', or 'count' query parameters were invalid or "
               "out of range.")


class InvalidStateAddress(_ApiError):
    api_code = 62
    status_code = 400
    title = 'Invalid State Address'
    message = ('The state address submitted was invalid. To fetch specific '
               'state data, you must submit the full 70-character address.')


class StatusIdQueryInvalid(_ApiError):
    api_code = 66
    status_code = 400
    title = 'Id Query Invalid or Missing'
    message = ("Requests for batch statuses sent as a GET request must have "
               "an 'id' query parameter with a comma-separated list of "
               "at least one batch id.")


class BlockNotFound(_ApiError):
    api_code = 70
    status_code = 404
    title = 'Block Not Found'
    message = ('There is no block with the id specified in the blockchain.')


class BatchNotFound(_ApiError):
    api_code = 71
    status_code = 404
    title = 'Batch Not Found'
    message = ('There is no batch with the id specified in the blockchain.')


class TransactionNotFound(_ApiError):
    api_code = 72
    status_code = 404
    title = 'Transaction Not Found'
    message = ('There is no transaction with the id specified in the '
               'blockchain.')


class StateNotFound(_ApiError):
    api_code = 75
    status_code = 404
    title = 'State Not Found'
    message = ('There is no state data at the address specified.')
