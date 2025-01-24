## Get the user list

### Request on the VPS

```bash
curl -X GET http://localhost:8000/users/
```

### Request on other machines

```bash
curl -k -X GET https://130.61.74.203/users/
```

### Response

```bash
{"users": [{"uuid": "28aa18bd-030b-4284-a03d-894477b13ccd", "email": "user@example.com", "password": "pbkdf2_sha256$870000$9YIU1MJRKIRFvtDW9FnCaj$y461K7CMR61RN+EPOmWnjbPaOqkT4yEkK2Ynhy4vhvQ=", "type": 3, "name": null, "address": null, "nationality": null, "request_membership": false, "phone": null, "state": true}, {"uuid": "a79dc0da-ea1d-4d4b-a45d-585d61452a47", "email": "another_user@example.com", "password": "pbkdf2_sha256$870000$038NjUk3b1AjsZSjfUP2Ko$QiGzgrkdEktI7YZ58z4mHC4tkaOTsZxJ7++ioYDdaBA=", "type": 2, "name": null, "address": null, "nationality": null, "request_membership": false, "phone": null, "state": true}]}%
```


## Create a new user

### Request on the VPS

```bash
curl -X POST http://localhost:8000/users/ -H "Content-Type: application/json" -d '{
    "email": "user@example.com",
    "password": "securepassword123"
}'
```

### Request on other machines

```bash
curl -k -X POST https://130.61.74.203/users/ -H "Content-Type: application/json" -d '{
    "email": "another_user@example.com",
    "password": "securepassword123"
}'
```

### Response

```bash
{"message": "User successfully created", "user_uuid": "28aa18bd-030b-4284-a03d-894477b13ccd"}
```


## Upgrade a user to member

### Request on the VPS

```bash
curl -X PUT http://localhost:8000/user/<user_uuid>/ -H "Content-Type: application/json"
```

### Request on other machines

```bash
curl -k -X PUT https://130.61.74.203/user/<user_uuid>/ -H "Content-Type: application/json"
```

### Response

```bash
{"message": "User successfully upgraded to member"}
```