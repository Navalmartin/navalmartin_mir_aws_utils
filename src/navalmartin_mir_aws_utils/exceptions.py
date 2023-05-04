from typing import List


class InvalidAWSClientException(Exception):
    def __init__(self, client_name: str, allowed_vals: List[str]):
        self.message = f"Client {client_name} is not a valid AWS client. Allowed values are {allowed_vals}"

    def __str__(self):
        return self.message


class PdfCreationException(Exception):
    def __init__(self, survey_id: str):
        self.message = f"An exception occurred while creating pdf for survey {survey_id}."

    def __str__(self):
        return self.message

