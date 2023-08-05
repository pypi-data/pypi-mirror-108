import boto3
import mimetypes

s3_resource = boto3.resource('s3')

def S3FileUpload(bucketName,s3KeyFilePath,localFilePath,contentType=" "):
    """
    bucketName    : The Object's bucket_name identifier. This **must** be set.
    s3KeyFilePath : S3 The Object's key identifier. This **must** be set. Example., "example-folder/filename.csv"
    localFilePath : File path in local directory.
    contentType   : content type of given file.
    """
    if contentType == " ":
        contentType, _ = mimetypes.guess_type(localFilePath)
        if contentType is None:
            raise Exception("Please mention contentType.")
    s3_resource.Object(bucketName,s3KeyFilePath).upload_file(Filename=localFilePath, ExtraArgs={'ContentType':contentType})
    return "Success"
