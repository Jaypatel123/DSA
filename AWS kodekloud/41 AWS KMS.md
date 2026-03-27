The Nautilus DevOps team is focusing on improving their data security by using AWS KMS. Your task is to create a KMS key and manage the encryption and decryption of a pre-existing sensitive file using the KMS key.

Specific Requirements:

Create a symmetric KMS key named xfusion-KMS-Key to manage encryption and decryption.
Encrypt the provided SensitiveData.txt file (located in /root/), base64 encode the ciphertext, and save the encrypted version as EncryptedData.bin in the /root/ directory.
Try to decrypt the same and verify that the decrypted data matches the original file.
Make sure that the KMS key is correctly configured. The validation script will test your configuration by decrypting the EncryptedData.bin file using the KMS key you created.


Use below given AWS Credentials: (You can run the showcreds command on aws-client host to retrieve these credentials)


### Solution

Step 1: Set Variables
KMS_KEY="devops-KMS-Key"
Step 2: Create a symmetric KMS key
Create symmetric KMS key

KEY_ID=$(aws kms create-key \
    --description "KMS key for encryption/decryption" \
    --key-usage ENCRYPT_DECRYPT \
    --origin AWS_KMS \
    --query "KeyMetadata.KeyId" \
    --output text)
Create alias for the Key

aws kms create-alias \
    --alias-name alias/$KMS_KEY \
    --target-key-id $KEY_ID
Step 3: Encrypt the file
aws kms encrypt \
    --key-id alias/$KMS_KEY \
    --plaintext fileb:///root/SensitiveData.txt \
    --output text \
    --query CiphertextBlob | base64 --decode > /root/EncryptedData.bin
Step 4: Decrypt the file to verify
aws kms decrypt \
    --key-id alias/$KMS_KEY \
    --ciphertext-blob fileb:///root/EncryptedData.bin \
    --output text \
    --query Plaintext | base64 --decode > /root/DecryptedData.txt
Check that the decrypted file matches the original

# If there is no output, the files match perfectly
diff /root/SensitiveData.txt /root/DecryptedData.txt