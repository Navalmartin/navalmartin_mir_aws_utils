from navalmartin_mir_aws_utils import AWSCredentials_SageMaker
from navalmartin_mir_aws_utils import get_aws_client_factory

if __name__ == '__main__':

    sagemaker_credentials = AWSCredentials_SageMaker(aws_region="eu-west-2")
    client = get_aws_client_factory(credentials=sagemaker_credentials)

    # create the model
    args = {'ModelName': "protonet_resnet18_vessel_classifier",
            "PrimaryContainer":{
                            'ContainerHostname': 'string',
                            'Image': 'string',
                            'ImageConfig': {
                                       'RepositoryAccessMode': 'Platform',
                                       'RepositoryAuthConfig': {
                                           'RepositoryCredentialsProviderArn': 'string'
                                       }
                            },
                            'Mode': 'SingleModel' | 'MultiModel',
                            'ModelDataUrl': 'string',
                            'Environment': {
                                       'string': 'string'
                            },
                            'ModelPackageName': 'string',
                                   'InferenceSpecificationName': 'string',
                                   'MultiModelConfig': {
                                       'ModelCacheSetting': 'Enabled' | 'Disabled'
                                   }
                            },
    }
    model_creation = client.create_model(**args)