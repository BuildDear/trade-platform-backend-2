# Generating RSA Key Pair (Private Key + Public Key)

## Using rsa Library in Python

```python
import rsa

# Generate a new RSA key pair with a size of 2048 bits
public_key, private_key = rsa.newkeys(2048)

# Save the public key to a file "public.pem" in PEM format
with open("public.pem", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))

# Save the private key to a file "private.pem" in PEM format
with open("private.pem", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))
```

# Or Using OpenSSL Utility in Command Line

## Generate an RSA private key with a size of 2048 bits
```
openssl genrsa -out jwt-private.ppk 2048
```

## Extract the public key from the key pair, which can be used in a certificate
```
openssl rsa -in jwt-private.ppk -outform PEM -pubout -out jwt-jwt-public.pem
```

This README.md provides instructions for generating an RSA key pair both in Python using the `rsa` library and through the command line using the OpenSSL utility. Each code block is accompanied by comments describing the actions performed, making it easier for users to understand and execute the instructions.
