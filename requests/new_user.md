```bash
curl -X POST http://localhost:8000/users/ -H "Content-Type: application/json" -d '{
    "email": "user@example.com",
    "password": "securepassword123"
}'
```