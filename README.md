## GET /user/ to see your settings
`` {
    "id": 3,
    "last_login": "2021-10-06T13:04:16.552861Z",
    "phone": 88005553535,
    "confirmed": false,
    "subscribed": false,
    "email": "example@example.com",
    "is_active": true,
    "is_admin": true,
    "role": {
        "id": 1,
        "role": "user"
    },
    "location": {
        "id": 59,
        "street": null,
        "house": null,
        "city": "Москва",
        "metro": null
    }
} ``
## POST /user/ to log in (get token)
`` {
    "username":"example@example.com"
    "password": "228322"


} ``
## PUT /user/ -to change your settings
`` {
    "phone": 88005553535,
    "email": "example@example.com"
    "role": "user"
    "street": null,
    "house": null,
    "city": "Москва",
    "metro": null

} ``
## POST /registration/ -to registration

### GET /metro/ -to see all moscow(for now) metro station
### POST /metro/ - to declare,special format

### GET /city/ -to see all russian cities
### POST /city// - to declare,special format


** all body can be also form-data **
