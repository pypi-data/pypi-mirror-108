import requests
import os
import json
import logging
import configparser
import boto3

from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)

CREATE_ACCOUNT_URL = "https://tksmt2n35c.execute-api.eu-west-1.amazonaws.com/accounts/create"
LOGIN_URL = "https://tksmt2n35c.execute-api.eu-west-1.amazonaws.com/accounts/login"
PROVISION_URL = "https://dev.aeroplatform.co.uk/compute/config"
PROFILE_NAME = "aero"
CLIENT_ID = "7qkl0rnt99f5nak775q1v99uv8"

class ComputeStatus():

    NO_VALUE = 0
    INIT = 1
    CREATING = 2
    CREATED = 3
    FAILED = 4

class Account():

    def __init__(self, email, auth_token, id_token):

        self.email = email
        self.auth_token = auth_token
        self.id_token = id_token

        self.user_home = str(Path.home())


    def provision(self):
        data = dict(
            company="solo",
            project="default"
        )
        logger.debug("provision()")
        logger.debug(data)
        r = requests.post(PROVISION_URL,
            json=data,
            headers = {
                "x-api-key": self.auth_token
            }
        )
        logger.debug(r.status_code)
        
        if r.status_code == 202:
            return ComputeStatus.INIT
        elif r.status_code == 207:
            return ComputeStatus.CREATING
        elif r.status_code != 200:
            raise Exception(r.status_code, r.text)

        response_data = r.json()

        response_data['config']['AERO_ID_TOKEN'] = self.id_token
        response_data['config']['AERO_IDENTITY_POOL'] = "eu-west-1:d9b38264-d2de-44cc-8812-7e48943f31ab"
        response_data['config']['AERO_PROVIDER'] = "cognito-idp.eu-west-1.amazonaws.com/eu-west-1_3E4bxVVbg"

        # Create Metaflow directory
        if not os.path.exists(f"{self.user_home}/.metaflowconfig"):
            os.mkdir(f"{self.user_home}/.metaflowconfig")

        with open(f"{self.user_home}/.metaflowconfig/config.json", 'w', encoding='utf-8') as f:
            json.dump(response_data['config'], f, ensure_ascii=False, indent=4)

        return ComputeStatus.CREATED
        

    @classmethod
    def login(cls, email, password):

        auth_token, id_token = cls._login(email, password)

        return Account(email, auth_token, id_token)

    @classmethod
    def create(cls, email, password):

        outcome = cls._create_account(email, password)

        return outcome
    
    @classmethod
    def _hash(cls, password):

        return sha256(password.strip()).hexdigest()

    @classmethod
    def _create_account(cls, email, password):

        data = dict(
            username=email, 
            password=password
        )
        logger.debug("_create_account()")
        logger.debug(data)
        logger.info("Signup is currently not supported on the CLI")

        return True

    @classmethod
    def _login(cls, email, password):

        cognito = boto3.client('cognito-idp')

        data = dict(
            email=email, 
            password=password
        )
        logger.debug("_login()")
        response = cognito.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password
            },
            ClientId=CLIENT_ID
        )

        if 'AuthenticationResult' not in response:
            raise Exception("Error logging in")

        logger.debug(response['AuthenticationResult']['AccessToken'])

        return response['AuthenticationResult']['AccessToken'], response['AuthenticationResult']['IdToken']
