## BLOG APP

- This is just a demo application, a blog application available as a tutorial on [flask website](https://flask.palletsprojects.com/en/1.1.x/tutorial/).
- Users will be able to register, log in, create, edit and delete posts.

### 1. The application factory
- A function that holds the falsk global instance.
- This will be created inside the [__init__.py](my_blog_app/__init__.py) file.
- Any configuration, registration and other setup the application needs takes place in there.

**Database :**
- This application uses an sqlite database, for simplicity because it is already included in python
- this will be changed to mysql, since as the requests grow, the speed might be affected.
