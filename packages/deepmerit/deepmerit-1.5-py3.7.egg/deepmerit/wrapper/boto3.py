import boto3
import mimetypes
import pandas as pd
from PIL import Image
from io import BytesIO
import pickle
import json
import s3fs
import h5py


def s3_upload_file(bucketName, key, localFilePath, contentType=" "):
    """
    bucketName    : Type - string | The Object's bucket_name identifier | **[REQUIRED]**  |
    key           : Type - string | S3 The Object's key identifier      | **[REQUIRED]**  | Example., "example-folder/filename.csv" |
    localFilePath : Type - string | File path in local directory        | **[REQUIRED]**  |
    contentType   : Type - string | content type of given file          |
    """
    s3_resource = boto3.resource('s3')

    if contentType == " ":
        contentType, _ = mimetypes.guess_type(localFilePath)
        if contentType is None:
            raise Exception("Please mention contentType.")
    s3_resource.Object(bucketName,key).upload_file(Filename=localFilePath, ExtraArgs={'ContentType':contentType})

def s3_read_csv(bucketName,key):
    """

    bucketName  : Type - string | The bucket name containing the object | **[REQUIRED]**  |
    key         : Type - string | Key of the object to get              | **[REQUIRED]**  |

    """
    client = boto3.client('s3') #low-level functional API
    obj = client.get_object(Bucket=bucketName, Key=key)
    data = pd.read_csv(obj['Body'])
    return data

def s3_read_image(bucketName,key):
    """

    bucketName  : Type - string | The bucket name containing the object | **[REQUIRED]**  |
    key         : Type - string | Key of the object to get              | **[REQUIRED]**  |

    """
    client = boto3.client('s3') #low-level functional API
    obj = client.get_object(Bucket=bucketName, Key=key)
    image = Image.open(BytesIO(obj['Body'].read()))
    return image

def s3_read_pickle(bucketName,key):
    """

    bucketName  : Type - string | The bucket name containing the object | **[REQUIRED]**  |
    key         : Type - string | Key of the object to get              | **[REQUIRED]**  |

    """
    client = boto3.client('s3') #low-level functional API
    obj = client.get_object(Bucket=bucketName, Key=key)
    model = pickle.loads(obj['Body'].read())
    return model

def s3_read_json(bucketName,key):
    """

    bucketName  : Type - string | The bucket name containing the object | **[REQUIRED]**  |
    key         : Type - string | Key of the object to get              | **[REQUIRED]**  |

    """
    s3 = boto3.resource('s3') #low-level functional API
    obj = s3.Object('vlife-portal','Metadata/json.json')
    json_file = json.load(obj.get()['Body'])
    return json_file

def s3_read_h5(s3FilePath):
    """

    s3FilePath  : Type - string | Object file path in s3         | **[REQUIRED]**  |

    """
    s3 = s3fs.S3FileSystem()
    file = h5py.File(s3.open(s3FilePath, "rb"))
    return file
