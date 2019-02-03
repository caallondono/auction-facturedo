# Auction System - Python developer

Simple API for auction and bids management.

## Installing

Create virtual environment and use requirements.txt for installing dependencies:

```
pip install -r requirements.txt
```

Run development server:

```
python manage.py runserver 0.0.0.0:8000
```


## API Docs

### 1. Test users:

* {“user”: 1, “username”: “admin”, “password”: “4dm1n123”}
* {“user”: 2, “username”: “user2”}
* {“user”: 3, “username”: “user3”}
* {“user”: 4, “username”: “user4”}

**Note**: This API has no restrictions. All applications can use it with no limits in permission levels.

### 2. Auctions

| Function  | Method | Endpoint  | Request data | Response data |
| ------------- | :---: | ------------- | ------------- | ------------- |
| Create auction  | POST  | /auction/  | **amount:** number | **id:** number <br> **amount:** number<br>**status:** string  |
| List auctions  | GET  | /auction/  | -  | [List]<br>**id:** number<br>**amount:** number<br>**status:** string  |
| Change auction status  | PUT  | /auction/change-status/<:id>  | **status:** string  | **id:** number<br>**amount:** number<br>**status:** string  |

### 3. Bids

| Function  | Method | Endpoint  | Request data | Response data |
| ------------- | :---: | ------------- | ------------- | ------------- |
| Create bid  | POST  | /auction/bid/  | **user:** number<br>**auction:** number<br>**amount:** number<br>**discount_rate:** number | **id:** number<br>**username:** string<br>**auction_id:** number<br>**auction_amount:** number<br>**amount:** number<br>**discount_rate:** number<br>**winner:** boolean  |
| List bids  | GET  | /auction/bid/  | -  | [List]<br>**id:** number<br>**username:** string<br>**auction_id:** number<br>**auction_amount:** number<br>**amount:** number<br>**discount_rate:** number<br>**winner:** boolean  |


## Running the tests

```
python manage.py test --verbosity=2
```

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django Rest Framework](https://www.django-rest-framework.org/) - Toolkit for building Web APIs

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Carlos Londoño** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
