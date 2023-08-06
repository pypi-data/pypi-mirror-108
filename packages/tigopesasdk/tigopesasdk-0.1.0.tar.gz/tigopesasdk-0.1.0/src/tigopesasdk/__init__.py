#  MIT License
#
#  Copyright (c) 2021 Pius Alfred
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

import json
from dataclasses import dataclass
from datetime import datetime
import abc
import requests
from flask_restful import Resource, reqparse


@dataclass(init=True)
class CallbackRequest:
    status: bool
    description: str
    reference_id: str
    mfs_transaction_id: str
    amount: str


def unmarshall_callback_request(request: dict) -> CallbackRequest:
    re = CallbackRequest(
        status=request["Status"],
        reference_id=request["ReferenceID"],
        amount=request["Amount"],
        description=request["Description"],
        mfs_transaction_id=request["MFSTransactionID"]
    )

    return re


@dataclass(init=True)
class CallbackResponse:
    response_code: str
    response_status: bool
    response_description: str
    reference_id: str

    def to_dict(self) -> dict:
        re = {
            "ResponseCode": self.response_code,
            "ResponseStatus": self.response_status,
            "ResponseDescription": self.response_description,
            "ReferenceID": self.reference_id
        }
        return re


class CallbackHandler(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(__obj=subclass, __name='respond') and
                callable(subclass.get) or
                NotImplemented
        )

    @abc.abstractmethod
    def respond(self, request: CallbackRequest) -> CallbackResponse:
        """:return User of the specified id"""
        raise NotImplementedError


class FlaskCallbackHandler(Resource):

    def __init__(self, responder: CallbackHandler):
        self.responder = responder

    parser = reqparse.RequestParser()

    parser.add_argument('Status', type=bool)
    parser.add_argument('Description', type=str)
    parser.add_argument('MFSTransactionID', type=str)
    parser.add_argument('ReferenceID', type=str)
    parser.add_argument('Amount', type=str)

    def post(self):
        data = FlaskCallbackHandler.parser.parse_args()
        request = unmarshall_callback_request(data)
        response = self.responder.respond(request)
        return response.to_dict(), 200


@dataclass(init=True)
class Debugger:
    message: dict
    timestamp: str
    method: str

    def loggable(self) -> dict:
        out = {
            "method": self.method,
            "timestamp": self.timestamp,
            "message": self.message
        }
        return out


@dataclass(init=True)
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: str


@dataclass
class BillPayRequest(object):
    customer_msisdn: str
    amount: int
    remarks: str
    reference_id: str


@dataclass(init=True)
class BillPayResponse:
    response_code: str
    response_status: bool
    response_description: str
    reference_id: str


@dataclass(init=True)
class Config:
    username: str
    password: str
    account_name: str
    account_msisdn: str
    brand_id: str
    biller_code: str
    token_url: str
    biller_payment_url: str
    grant_type: str = "password"


@dataclass(init=True)
class TigoClient(object):
    """
    The client responsible for making calls to TigoPesa gateway.
    It contains configurations that are obtained during integration stage and
    a debug mode which is false per default
    """
    config: Config
    callback_handler: CallbackHandler
    debug: bool = False

    def bill(self, req: BillPayRequest) -> BillPayResponse:
        """
        Args:
            req: the billpay request

        Returns:
            billpay response or None if the request fails
        """
        token_response = self.generate_token()
        if token_response is None:
            return None
        return self.bill_with_token(token_response.access_token, req)

    def bill_with_token(self, token: str, req: BillPayRequest) -> BillPayResponse:
        data = {
            "CustomerMSISDN": req.customer_msisdn,
            "BillerMSISDN": self.config.account_msisdn,
            "Amount": int(req.amount),
            "Remarks": req.remarks,
            "ReferenceID": req.reference_id,
        }

        bearer_token = "bearer " + token

        headers = {
            "Username": self.config.username,
            "Password": self.config.password,
            "Authorization": bearer_token,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }

        response = requests.post(
            url=self.config.biller_payment_url,
            headers=headers,
            json=data,
        )

        json_response = response.json()

        billpay_resp = BillPayResponse(
            response_code=json_response["ResponseCode"],
            reference_id=json_response["ReferenceID"],
            response_status=json_response["ResponseStatus"],
            response_description=json_response["ResponseDescription"]
        )

        if self.debug is True:
            method = "bill with token"
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            message = {
                "biller_url": self.config.biller_payment_url,
                "headers": headers,
                "data": data,
                "response": json_response
            }
            debug_info = Debugger(
                timestamp=timestamp,
                method=method,
                message=message
            )
            json_object = json.dumps(debug_info.loggable(), indent=4)

            # todo: change this to appropriate logger
            print(json_object)

        return billpay_resp

    def generate_token(self) -> TokenResponse:
        """
        ask for access token from tigo

        Returns:
            str: access token used for push pay requests
        """
        data = {
            "username": self.config.username,
            "password": self.config.password,
            "grant_type": self.config.grant_type
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache"
        }

        response = requests.post(
            url=self.config.token_url,
            headers=headers,
            data=data
        )

        if self.debug is True:
            method = "generate token"
            json_response = response.json()
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            message = {
                "biller_url": self.config.biller_payment_url,
                "headers": headers,
                "data": data,
                "response": json_response
            }
            debug_info = Debugger(
                timestamp=timestamp,
                method=method,
                message=message
            )
            json_object = json.dumps(debug_info.loggable(), indent=4)

            # todo: change this to appropriate logger
            print(json_object)

        if response.status_code.real >= 400:
            return None
        else:
            json_response = response.json()
            token_response = TokenResponse(
                access_token=json_response['access_token'],
                token_type=json_response['token_type'],
                expires_in=json_response['expires_in']
            )
            return token_response
