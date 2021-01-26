# PostAnything
This Project deals with handling of online posts.

Project Details 

- Admin can create/delete account for users.
- Users can login via password shared by admin.
- Passwords are stored in hashes in database for sequrity reasons
- Users can update the account (update name/email/password).
- Users can add/update/delete posts.
- No database is used, all data are stored in memory (local object)


How to run api server
1. Need python3 to run
2. git clone project (`git clone https://github.com/vibhavsharma341/PostAnything.git`)
3. `cd PostAnythong/post_anything`
4. `pip install -r requirements.txt`
5. `python app.py`


list of apis :

**admin apis**

1. add a user

    sample : 
    add a user jhon

        curl --location --request POST 'http://localhost:5000/user/add' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "user_id" : "jhon",
            "name" : "jhon",
            "email" : "jhon@gmail.com",
            "password" : "jhon2020"
        }'


2. get all the users 

`curl --location --request GET 'http://localhost:5000/users'`

3. get the user detail

sample :
to see user jhon details

`curl --location --request GET 'http://localhost:5000/users/jhon'`



**User APIS**

1. update the user details 

    sample:
    update the details for jhon (*need to provide old password to update the details*)
        
        curl --location --request PUT 'http://localhost:5000/user/update' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "user_id" : "jhon",
            "name" : "jhon",
            "email": "jhon@gmail.com",
            "password_old" : "jhon2020",
            "password_new" : "jhon2020"
        }'


2. login user

    sample:
    login jhon
        
        curl --location --request POST 'http://localhost:5000/user/login' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "user_id": "jhon",
            "password": "jhon2020"
        }'


3. add a post 

    sample
    add a post for jhon
        
        curl --location --request POST 'http://localhost:5000/user/add/post' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "user_id": "jhon",
            "post_id": "1",
            "post": "I am feeling good"
        }'
        

4. update a post 

    sample 
    update a post for jhon
        
        curl --location --request PUT 'http://localhost:5000/user/update/post' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "user_id": "jhon",
            "post_id": "1",
            "post": "I am lucky"
        }'

5. get all post 

    sample
    get all post for jhon
        
        curl --location --request GET 'http://localhost:5000/user/posts/jhon'
        

6. delete a post, sample 
        
        curl --location --request DELETE 'http://localhost:5000/user/jhon/delete/post/1'
