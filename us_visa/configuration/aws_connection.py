import boto3
import os
from us_visa.constants import AWS_SECRET_ACCESS_KEY_ENV_KEY, AWS_ACCESS_KEY_ID_ENV_KEY, REGION_NAME


class S3Client:
    """
    This class manages an S3 connection using AWS credentials from environment variables.
    It creates a singleton connection with the S3 client and resource.
    """
    s3_client = None
    s3_resource = None

    def __init__(self, region_name=REGION_NAME):
        """
        Initializes the S3 client and resource using credentials from environment variables.
        Raises an exception if the required environment variables are not set.
        """
        try:
            # Check if the client and resource are already initialized
            if S3Client.s3_resource is None or S3Client.s3_client is None:
                # Retrieve credentials from environment variables
                access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
                secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)

                if access_key_id is None:
                    raise EnvironmentError(f"Environment variable '{AWS_ACCESS_KEY_ID_ENV_KEY}' is not set.")
                if secret_access_key is None:
                    raise EnvironmentError(f"Environment variable '{AWS_SECRET_ACCESS_KEY_ENV_KEY}' is not set.")

                # Initialize the S3 resource and client
                S3Client.s3_resource = boto3.resource(
                    's3',
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    region_name=region_name
                )
                S3Client.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    region_name=region_name
                )

            # Assign the initialized objects to instance variables
            self.s3_resource = S3Client.s3_resource
            self.s3_client = S3Client.s3_client

        except Exception as e:
            raise Exception(f"Failed to initialize S3 client or resource: {str(e)}")


        