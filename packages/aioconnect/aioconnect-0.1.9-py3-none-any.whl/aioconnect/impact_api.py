from numpy import info
import requests
from requests import Request, Session

import io
import pandas as pd
from datetime import datetime
import json
from aioconnect.helpers import *
from dotenv import load_dotenv
from os import getenv


def get_list(
    token: str,
    object: str = "dotTypes",
    key: str = "_id",
) -> list:
    """Get List of values for a key of an object of the API.

    Parameters
    ----------
    token : str
        Token which was returned from the user login.
    object : str = "dotTypes"
        Object to be extracted from the API.
    key : str = "_id"
        Key of the DOT.

    Returns
    -------
    list
        Values for the provided key of the object.

    Raises
    ------
    KeyError
        In case there was an object type given which does not exist.
    """
    url = getenv("CONNECT_URL")
    json_data = get_object(token=token, object=object)

    return get_values(json_data=json_data, key=key)


def get_object(
    token: str,
    object: str = "digitalObjectTwins",
) -> list:
    """Get JSON object.

    Parameters
    ----------
    token : str
        Token which was returned from the user login.
    object : str = "dotTypes"
        Object to be extracted from the API.

    Returns
    -------
    list
        List of JSON objects.

    Raises
    ------
    KeyError
        Raises KeyError when the input is not correct.
    """
    url = getenv("CONNECT_URL")

    if object == "digitalObjectTwins":
        url += "/digitalObjectTwins/"
    elif object == "measures":
        url += "/measures/"
    elif object == "initiatives":
        url += "/initiatives/"
    else:
        raise KeyError

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.request("GET", url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_token(
    email: str,
    password: str,
):
    """Log into AIO Impact and get a token.

    Parameters
    ----------
    email : str
        Email address of the user account.

    password : str
        Password of the user account.

    Returns
    -------
    str
        Bearer token.

    Raises
    -------
    requests.exceptions.HTTPError
        If the username and password are wrong.

    Examples
    --------
    >>> aioconnect.get_token(
    >>>     email="firstname.lastname@aioneers.com", password="xxx",
    >>> )
    """

    url = getenv("CONNECT_URL") + "/login/"
    payload = json.dumps({"email": email, "password": password})
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()

    token = response.json()["token"]

    return token


# def create_DOT(
#     token: str,
#     DOT_name: str,
#     DOT_baseline: float,
#     DOT_description: str = None,
#     DOT_type_id: str = "6019fa2072b96c00133df326",
#     METRIC_type_id: str = "5fb7bf2f8ce87f0012fcc8f3",
# ):
#     """
#     Create a new DOT in AIO Impact.

#     Parameters
#     ----------
#     token : str
#         Token which was returned from the user login.

#     DOT_name : str
#         Name of the DOT.

#     DOT_baseline : float
#         Baseline value of the DOT.

#     DOT_description : str = DOT_name
#         Description of the DOT.

#     DOT_type_id : str = "6019fa2072b96c00133df326"
#         ID of the DOT type.

#     METRIC_type_id : str = "5fb7bf2f8ce87f0012fcc8f3"
#         ID of the METRIC type.

#     Returns
#     -------

#     requests.Response
#         HTTP response.

#     Examples
#     --------
#     >>> token = aioconnect.get_token(
#     >>> email="firstname.lastname@aioneers.com", password="xxx",
#     >>> )
#     >>>
#     >>> res = aioconnect.create_DOT(
#     >>>     token=token,
#     >>>     DOT_name="TEST_DOT",
#     >>>     DOT_description="TEST_DOT description",
#     >>>     DOT_baseline=1234,
#     >>>     DOT_type_id="6019fa2072b96c00133df326",
#     >>>     METRIC_type_id="5fb7bf2f8ce87f0012fcc8f3",
#     >>> )
#     """

#     if DOT_description == None:
#         DOT_description = DOT_name

#     url = getenv('CONNECT_URL') + "​/digitalObjectTwins​"
#     url = url.rstrip("/")

#     payload = json.dumps(
#         {
#             "name": DOT_name,
#             "description": DOT_description,
#             "type": DOT_type_id,
#             "baseline": DOT_baseline,
#             "metricType": {"_id": METRIC_type_id},
#         }
#     )
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/json",
#     }

#     response = requests.post(url=url, headers=headers, data=payload)
#     response.raise_for_status()

#     return response


def upsert_DOT(
    token: str,
    dataframe: pd.DataFrame,
) -> list:
    """Create a new DOT in AIO Impact or update it if the DOT is already existing.

    Parameters
    ----------
    token : str
        Token which was returned from the user login.

    dataframe : Pandas.DataFrame
        Dataframe containing DOT details.

    Returns
    -------
    requests.Response
        HTTP response.

    Examples
    --------
    >>> token = aioconnect.get_token(
    >>> email="firstname.lastname@aioneers.com", password="xxx",
    >>> )
    >>> res = aioconnect.upsert_DOT(
    >>>     token=token,
    >>>     dataframe = df
    >>> )
    """

    url = getenv("CONNECT_URL") + "/digitalObjectTwins/"
    url = url.rstrip("/")

    columns_list = [
        "externalID",
        "name",
        "metricType",
        "actuals",
    ]

    if all([item in dataframe.columns for item in columns_list]):
        payload = dataframe.to_json(orient="records")

        response = requests.put(
            url=url, headers={"Authorization": f"Bearer {token}",
                              'Content-Type': 'application/json'}, data=payload)
        response.raise_for_status()

        return response
    else:
        raise KeyError("Columns not correct")
