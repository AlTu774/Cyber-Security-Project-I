Instructions: clone github repository https://github.com/AlTu774/Cyber-Security-Project-I
and start the server with “python3 manage.py runserver” in /website directory. This will start the server and the simple blog app index page is /blog/.


FLAW 1: OWASP Top 7: Identification and Authentication Failures,
CWE-521: Weak Password Requirements
https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/blog/views.py#L23-L38
The application has weak password vulnerability in the views/create_new_user. There are no password validators, so the website allows for any type of password to be registered with a new user. This puts the users at risk of credential stuffing and brute force attacks where common password are tried on the user registration form to gain access to user accounts with weak passwords.

<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-1-before-1.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-1-before-2.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-1-before-3.png>

FIX 1: This can be fixed by adding validators. In the fix, the blog app uses Django’s predefined form, UserCreationForms to handle the creation of new users. Through this form, Django has password validators by default, and these validators are defined in the settings.py file under ‘AUTH_PASSWORD_VALIDATORS’ setting. The validators require the password to have minimum length (9 character), and to contain only certain characters and numbers, and for the password to not be in a list of 20,000 common easy passwords, or for it to not be entirely numeric.

https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/website/settings.py#L91
https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/blog/views.py#L41
https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/blog/templates/blog/user_creation.html#L24

<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-1-after-1.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-1-after-2.png>

Using validators is at least a decent enough fix for this application. Relying on just a password might not be enough for a more robust website, so adding something like multi factor authentication would give more security than just a strong password.


FLAW 2: OWASP Top 1: Broken Access Control,
CWE-284: Improper Access Control
https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/blog/views.py#L140

Anyone can delete blogs from any of the users’ user page. This isn’t the intended purpose since only the creator of a blog should be able to delete said blog. On every user page there is also a link to a form for creating new blogs and anyone can click these. A blog can only be created by a logged in user and the blog is added to said user’s user page, but the creation form should still be visible only to a logged in user on their user page.

<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-2-before-1.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-2-before-2.png>

FIX 2: In the app the problem is fixed by making sure that the delete function checks that user trying to delete the blog (the logged in user request.user) is the same as the user that created the blog (blog.user). Also the create blog link and delete buttons are hidden if someone other than the user themselves is viewing the user page. Also for all the views that require an user to be logged in, Django’s ‘@login_required’ decorator is used to make sure that anyone trying to use functionalities for users is actually logged in and authenticated.

https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/blog/views.py#L76
https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/blog/views.py#L147

<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-2-after-1.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-2-after-2.png>

It doesn’t show in the pictures, but if user1 tries to delete user2’s blog  by going to  “/blog/<id:int>/delete” it will redirect user2 to user2’s user page and won’t delete the blog.



FLAW 3: OWASP Top 3: Injection,
CWE-89: SQL injection

https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/blog/views.py#L127

The creation of a new comment is implemented in a way that makes it susceptible to SQL injections. With Django’s ‘connections’ function one can send raw SQL queries and skip ORM protection completely. Also since user inputs are directly added into the query they are not parameterized, meaning that user input could be interpreted as part of the SQL query.

<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-3-before-1.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-3-before-2.png>

FIX 3: Instead of directly interacting with sqlite, making changes to the database through Django’s models fixes the problem. When a new comment is added through the Comment model with ‘Comment(user=user, blog=blog, text=text).save()’, Django uses ORM (Object-Relational Mapper) to parameterize the user inputs in the query so that they won’t be executed as SQL code. Another fix could be to change the query in the flawed implementation to “  c.execute("INSERT INTO blog_comment (user_id, blog_id, text) VALUES (?, ?, ?);", (user.id, blog.id, text))  ”, which only executes one query and parameterizes the query.

https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/blog/views.py#L111

<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-3-after-1.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-3-after-2.png>


FLAW 4: Cross Site Request Forgery (CSRF)
This wasn’t in the 2021 OWASP top 10 list but it was allowed as a flaw for the project. Blog creation form doesn’t contain protection against CSRF and it also sends blog’s form field data through GET method and not through POST. If a user is logged in and thus authenticated, they will have a sessionid cookie on their browser. If the same user then happens to visit a malicious website, it can initiate a CSRF attack by sending a GET request to blog/confirm_blog page with the user’s sessionid and then create a blog.

<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-4-before-1.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-4-before-2.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-4-before-3.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-4-before-4.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-4-before-5.png>

FIX 4: This can be fixed easily by adding “{% csrf_token %}” to any form, which Django’s csrf middleware will use to make sure the request comes from the right place (blog/blog_form’s form) and changing the GET to POST method (now the simple img tag can’t initiate blog creation). Also in the website/settings.py file the lines SESSION_COOKIE_SAMESITE = 'None' and
SESSION_COOKIE_SECURE = True should be commented out, since the settings will allow session cookies to come from different sites and also assumes all session cookies to be secure.

https://github.com/AlTu774/Cyber-Security-Project-I/blob/5279779c10c37f5beec76d5fc57f5c86d2552442/website/blog/templates/blog/blog_form.html#L4
https://github.com/AlTu774/Cyber-Security-Project-I/blob/5279779c10c37f5beec76d5fc57f5c86d2552442/website/blog/views.py#L102
https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/website/settings.py#L132

<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-4-after-1.png>


FLAW 5: OWASP Top 2: Cryptographic Failures,
CWE-759: Use of a One-Way Hash without a Salt 

The way that the passwords are hashed is not cryptographically secure. The users’ passwords are not stored in plaintext on the database, but the algorithm used to hash the passwords is not secure. Django’s hash setting is set to use an unsalted MD5 hasher, which is not up to modern standards. This puts users passwords at risk, since exposed hashed passwords can be cracked fairly easily.

<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-5-before-1.png>
<img src=https://github.com/AlTu774/Cyber-Security-Project-I/blob/main/screenshots/flaw-5-before-2.png>

FIX 5: Using a more secure hasher will make the passwords harder to crack. The fix is easy, since by default the Django framework uses a more secure PBKDF2 algorithm with a SHA256 hash, so just removing the list “PASSWORD_HASHERS” in settings.py will default the app to use PBKDF2.

https://github.com/AlTu774/Cyber-Security-Project-I/blob/6db1f0b1d0550b494a16d88af3a878ee9e5c1790/website/website/settings.py#L142
