# SMS.RU python library

## Usage example

```python
from smsru_sender import SMSruSender

phone = '+79508887766'
response = SMSruSender().send(phone, f"Your confirmation code is 1234")
if not response.success:
    print(response.status_message)
```
