import unittest
import requests_mock
import requests
import pytest
from api_data import get_people, create_contact, transform_data


class TestAPIFunctions(unittest.TestCase):
    """
    Note : I've decided to use mocks to test the API for 2 reasons :
    - it's usually the best practice when testing an API
    - my tests won't spam your API 
    Obviously, that means that I'm testing what's returned by my mock, and not your actualy API.
    """
    def test_get_people_success(self):
        # Given
        person_1 = {
            "id": '1',
            "fields": {
                "firstName": 'john',
                "lastName": 'doe',
                "dateOfBirth": '02-02-2020',  # formatting "mm-dd-yyyy"
                "email": 'johndoe@email.com',
                "lifetimeValue": '$200.0'  # formatting "$xx.xx" 
            }
        }
        person_2 = {
            "id": '2',
            "fields": {
                "firstName": 'jane',
                "lastName": 'doe',
                "dateOfBirth": '02-02-2021',  # formatting "mm-dd-yyyy"
                "email": 'janedoe@email.com',
                "lifetimeValue": '$201.0'  # formatting "$xx.xx" 
            }
        }
        expected_people = [person_1, person_2]
        with requests_mock.Mocker() as mock:
            mock.get("https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app/people/", json=expected_people, status_code=200)
            # Do
            people = get_people()
            # Assert
            self.assertEqual(expected_people, people)

    def test_get_people_failure(self):
        # Govien
        with requests_mock.Mocker() as mock:
            mock.get("https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app/people/", status_code=400)
            # Do
            with self.assertRaises(Exception) as context:
                get_people()
            # Assert
            self.assertEqual("Failed to get people data.", str(context.exception))

    def test_create_contact_success(self):
        # Given
        contact = {
            "first_name": "John",
            "last_name": "Doe",
            "birthdate": "2000-01-01",
            "email": "johndoe@example.com",
            "custom_properties": {
                "airtable_id": "rec1",
                "lifetime_value": 100.0
            }
        }
        expected_response = {"message": "Contact created successfully"}
        with requests_mock.Mocker() as mock:
            mock.post("https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app/contacts/", json=expected_response, status_code=200)
            # Do
            response = create_contact(contact)
            # Assert
            self.assertEqual(expected_response, response)

    def test_create_contact_failure(self):
        # Given
        contact = {
            "first_name": "John",
            "last_name": "Doe",
            "birthdate": "2000-01-01",
            "email": "johndoe@example.com",
            "custom_properties": {
                "airtable_id": "rec1",
                "lifetime_value": 100.0
            }
        }
        with requests_mock.Mocker() as mock:
            mock.post("https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app/contacts/", status_code=400)
            # Do
            with self.assertRaises(Exception) as context:
                create_contact(contact)
            # Assert
            self.assertEqual("Failed to create contact.", str(context.exception))

    def test_transform_data_success(self):
        # Given
        people = [{
            "id": "rec1",
            "fields": {
                "firstName": " John ",
                "lastName": " Doe ",
                "dateOfBirth": "01-01-2000",
                "email": "johndoe@example.com",
                "lifetimeValue": "$100.00"
            }
        },
        {
            "id": "rec2",
            "fields": {
                "firstName": " Jane ",
                "lastName": " Doe ",
                "dateOfBirth": "02-02-2010",
                "email": "janedoe@example.com",
                "lifetimeValue": "$200.00"
            }
        }]
        expected_contacts = [{
            "first_name": "John",
            "last_name": "Doe",
            "birthdate": "2000-01-01",
            "email": "johndoe@example.com",
            "custom_properties": {
                "airtable_id": "rec1",
                "lifetime_value": 100.0
            }
        },
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "birthdate": "2010-02-02",
            "email": "janedoe@example.com",
            "custom_properties": {
                "airtable_id": "rec2",
                "lifetime_value": 200.0
            }
        }]
        # Do
        contacts = transform_data(people)
        # Assert
        self.assertEqual(expected_contacts, contacts)
