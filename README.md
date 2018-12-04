# Test Arcane:Real estate management restful API using Flask

This repository is a RESTful API using the Flask web framework and MongoDB database. Among the included features we'll see how to :
- Install the application
- Register/login into the server
- Manage your profile (edit user)
- Manage your properties (add, edit and delete a property)




### Install the application

Clone the git repository

```
$ git clone https://github.com/rmotr/flask-api-example.git
$ cd TestArcane
```

Create the virtualenv

```
$ mkvirtualenv TestArcane
```

Install dependencies
```
$ pip install -r requirements.txt
```

Run the app
```
$ python run_app.py
```

Note: to use this API, you can use an API testing tool such as Insomnia or Postman in order to send the requests.

## Running the tests


### Register/login into the server
You can view all the users registered by send a GET request to /users

First, register using a POST request to the /register route with a Content-Type: application/json. The password will be hashed and put into the database.
```
{
	"First Name": "Maxime",
	"Last Name": "BOUN" ,
	"Username": "maximeboun",
	"Password":"helloworld",
	"Date of birth" : "28/08/1996"
}

```

Then log into your account using a POST request to /login:

```
{
	"Username": "maximeboun",
	"Password":"helloworld"
}
```

To logout, just send a GET request to /logout. 



### Manage your user profile (edit and delete an user)

Make sure you are connected first. Then, send a POST request with the fields to be modified:

```
{
	"First Name":"Jean",
	"Last Name":"Dupont",
	"Password":"1234"
}
```

###  Manage your properties

To view all the properties, send a GET to /properties. To show properties in a particular city, send a POST to /cityproperties:

```
{
	"city":"Paris"
}
```

To edit your property, make sure you are connected. Then send a POST to /editproperty: 

```
{
	"Name": "test edit"
	"Type": "Studio"
}
```
To delete your property, send a GET to /deleteproperty.



