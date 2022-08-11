## Introduction

Sloovi assesment test. Performs basic CRUD and uses JWT for authentication.

### Getting started
You can create a fork or clone this repo directly to download the code to your local repository

    git clone https://github.com/KeneNwogu/sloovi-assesment-test
    cd sloovi-assesment-test

#### Installation and Prerequisites
The following prerequisites are required to run the project locally:

 - Python
 - MongoDb

	 #### Project dependencies: Before running the application, some project dependencies need to be installed and these are located in the requirements.txt file. To install each requirement, run:

	`pip install -r requirements.txt`

#### Environment Variables
The following environment variables are needed to properly run the application without any errors. These will be divided into sections to according to their purpose(s):

##### DATABASE ENVIRONMENT VARIABLES
These variables are required to connect the API to your local or production database. MongoDb or a remote Mongo Database cluster must be available to move forward with the project installation.

 1. MONGO_URI: This represents the database uri the backend uses to connect to the database

### Running Locally
To run the project locally, while you're in the sloovi-assesment-test directory, run:

`python wsgi.py`

**Note: All prerequisites should be completed**

### Documentation
The API is split into 2 resources: Users and Templates. The users blueprint is responsible for authentication
and the templates blueprint handles the CRUD for the templates' collection.

**Note: All endpoints require a Content-Type header that is set to** ***application/json***

#### Users:
This section covers all user related endpoints

1. **/register - (POST request)**

This endpoint handles registering of users. It adds a new field to the user collection if
the email does not exist

##### Request Body:
     {
         "email": <email: string>, // required
         "first_name": <string>, // required
         "last_name": <string>, // required
         "password": <string> // required
     }
     
##### Response Body:
     {
            "success": True,
            "message": "successfully registered user",
            "email": <email>
     }
<br> 
   
**/login - (POST request)**
This endpoint handles authentication of users. It returns a new jwt.

##### Request Body:
     {
         "email": <email: string>, // required
         "password": <string> // required
     }
     
##### Response Body:
     {
            "message": "successfully logged in user",
            "token": "<jwt>"
     }
<br>    
     
#### Templates:
This section covers all template related endpoints
**Note: All endpoints require authentication by setting the Authorization header in the form:**
    
    `headers: { Authorization: Bearer + <token> }`
    
  This token can be gotten from the /login endpoint
    


**/template - (GET request)**

This endpoint returns all templates belonging to the authenticated user.

##### Response Body:
     [
            {
                "template_name": "Example",
                "subject": "Example Template response",
                "body": "Example template body"
            }
     ]
<br>
     
**/template - (POST request)**
This request creates a new template for user
##### Request Body:
     {
        "template_name": "Example", // required
        "subject": "Example Template response", // required
        "body": "Example template body" // required
     }
     
##### Response Body:
    {
        "success": True, 
        "message": "successfully created template", 
        "template_id": <template_id_string>
    }
<br>
    
**/template/<template_id> - (GET request)**
This endpoint returns the template of the user that has the given template_id param
##### Response Body:
     {
        "template_name": "Example", // required
        "subject": "Example Template response", // required
        "body": "Example template body" // required
     }
<br>
     
**/template/<template_id> - (PUT request)**
This endpoint changes the values of the template to the new ones provided.

##### Request Body:
     {
        "template_name": "Example", // required
        "subject": "Example Template response", // required
        "body": "Example template body" // required
     }
     
##### Response Body:
    {
        "success": True, 
        "message": "successfully updated template", 
    }
<br>

**/template/<template_id> - (DELETE request)**
This endpoint deletes the template with the given id
##### Response Body:
    {
        "success": True, 
        "message": "successfully deleted template"
    }
    

