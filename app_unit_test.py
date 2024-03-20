import unittest
import hashlib
from unittest.mock import patch, MagicMock
from app import lambda_handler, validate_hash_md5, store_information_dynamo, delete_file

class TestLambda(unittest.TestCase):

    def test_validate_hash_md5(self):
        string_values_base = "test"
        hash_md5_compare = hashlib.md5(string_values_base.encode('utf-8')).hexdigest()
        self.assertTrue(validate_hash_md5(string_values_base, hash_md5_compare))

        string_values_base = "test"
        hash_md5_compare = "incorrect_hash"
        self.assertFalse(validate_hash_md5(string_values_base, hash_md5_compare))

    @patch('boto3.client')
    def test_lambda_handler(self, mock_boto3_client):
        # Configura el mock para simular la respuesta de boto3.client
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        mock_s3.get_object.return_value = {'Body': MagicMock(read=MagicMock(return_value='key=value\nhash=hash_value'))}

        # Prueba lambda_handler con un evento de prueba
        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {'name': 'test_bucket'},
                        'object': {'key': 'test_key'}
                    }
                }
            ]
        }
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 500)

    @patch('boto3.resource')
    def test_store_information_dynamo(self, mock_boto3_resource):
        # Configura el mock para simular la respuesta de boto3.resource
        mock_dynamodb = MagicMock()
        mock_boto3_resource.return_value = mock_dynamodb
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table

        # Prueba store_information_dynamo con un map_file de prueba
        map_file = {'key': 'value', 'hash': 'hash_value'}
        self.assertTrue(store_information_dynamo(map_file))

    @patch('boto3.resource')
    def test_delete_file(self, mock_boto3_resource):
        # Configura el mock para simular la respuesta de boto3.resource
        mock_s3 = MagicMock()
        mock_boto3_resource.return_value = mock_s3
        mock_object = MagicMock()
        mock_s3.Object.return_value = mock_object

        # Prueba delete_file con un bucket y key de prueba
        self.assertEqual(delete_file('test_bucket', 'test_key'), 1)

if __name__ == '__main__':
    unittest.main()