### Request

```bash
curl -X POST http://localhost:8000/users/ -H "Content-Type: application/json" -d '{
    "email": "user@example.com",
    "password": "securepassword123"
}'
```

### Response

```bash
{"message": "User successfully created", "user_uuid": "28aa18bd-030b-4284-a03d-894477b13ccd"}
```

curl -X POST https://130.61.74.203/users/ -H "Content-Type: application/json" -d '{
    "email": "another_user@example.com",
    "password": "securepassword123"
}'