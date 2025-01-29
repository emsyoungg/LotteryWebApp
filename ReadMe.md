Lottery Web App

This is a web app that allows users to play a simple lottery game. Users can register and login, create draws of 6 numbers (1-60), submit it and wait to see if they have won. <br>
Admins are able to create a randomised winning draw which the users' draws are compared against. Only admins can register new admins. A default admin account for testing can  <br>
The focus of this project is to focus on implementing secure coding practices and to ensure that the app is secure and free from vulnerabilities.  <br>
To run the app locally, clone the repository and run the following command in the terminal:
```
flask run --cert=adhoc
```
The app will be running on https://127.0.0.1:5000/ in your browser.

If a site not secure warning appears, click on the advanced button and proceed to the site. This is just because I have implemented a dummy SSL certificate for the app.

Default Admin Account: <br>
email='admin@email.com', <br>
password='Admin1!', <br>
firstname='Alice', <br>
lastname='Jones', <br>
phone='0191-123-4567', <br>
date_of_birth='01/01/2001', <br>
postcode='DN2 7NY', <br>
role='admin' <br>
You will need to set up a time-based PIN by in an authenticator app using the pin-key 4Q6R633272T45J6IDNPEWX3JQTQAIEUY 

Requirements: <br>

| Element | Requirement |
|---------|------------|
| **1.1** | **Registration Page** |
|         | Username must only be a valid email address |
| **1.2** | **Registration Page** |
|         | Firstname and Lastname must not contain the characters: * ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < > |
| **1.3** | **Registration Page** |
|         | Phone number must be a String containing only digits (X) and dashes (-) of the form: XXXX-XXX-XXXX |
| **1.4** | **Registration Page** |
|         | Password must only be between 6 and 12 characters in length |
|         | Password must contain at least 1 digit, at least 1 lowercase and at least 1 uppercase word character |
|         | Password must contain at least 1 special character (a non-alphanumeric character - not an alphabetic or numerical character) |
| **1.5** | **Registration Page** |
|         | Confirm password must match Password (Sub-task 1.4) |
| **1.6** | **Registration Page** |
|         | All registration data must be provided |
|         | Appropriate validation error messages must be shown for all registration data |
| **1.7** | **2 Factor Authentication Setup Page** |
|         | Once registration is complete, a new user should be redirected to a 2 Factor Authentication Setup page |
|         | 2FA Setup page should contain a scannable QR code and instructions for setting up an account on an authenticator application |
|         | 2FA Setup page should contain a link to the Login page |
| **1.8** | **Date of Birth** |
|         | Must be a String containing only appropriate digits* and forward slashes (/) of the form: DD/MM/YYYY - D (Day), M (Month), Y (Year). |
| **1.9** | **Postcode** |
|         | Must be a String containing only uppercase letters (X) and digits (Y) of the following forms: XY YXX, XYY YXX, XXY YXX |
| **1.10** | **All New Registration Data** |
|         | All registration data from requirements 1.8 and 1.9 must be provided |
|         | Appropriate validation error messages must be shown for all registration data from requirements 1.8 and 1.9 |
| **2.1** | **Error Pages** |
|         | An error page to be rendered for each error containing only the error code and error name |
|         | Each error page must include a message containing a short explanation of the error |
|         | Each error page must contain a link to an external web page explaining the error code |
| **3.1** | **Login Page** |
|         | A login form containing the following data fields: Username (email address), Password, Time-based PIN, reCAPTCHA, Login button |
| **3.2** | **Authentication Process** |
|         | Login attempts limited to 3 |
|         | Submitted Username, Password and Time-based PIN must be compared/validated against existing data in the database |
|         | Authenticated users must be logged into the application (i.e., no longer anonymous) |
| **3.3** | **Login Form** |
|         | All login data must be provided |
|         | Appropriate error messages must be shown for invalid logins |
|         | Login error message must show allowed login attempts remaining |
| **3.4** | **Logout Link** |
|         | Logged in users are logged out of the application (i.e., made anonymous) and redirected to the home (index) page |
| **3.5** | **N-Factor Authentication** |
|         | Login form extended to contain a Postcode data field |
|         | Authentication process extended by also comparing/validating Postcode against existing data in the database |
| **4.1** | **Anonymous (logged out)** |
|         | Can only see links for Home page, Register page, and Login page |
|         | Can only access Home page, Register page, Setup 2FA page, Login page and all their functions |
| **4.2** | **User (logged in)** |
|         | Redirected to Lottery page containing user's firstname once authenticated |
|         | Can only see links for Home Page, Lottery page, Account page, and Logout |
|         | Can only access Lottery page and all its functions, Account page, Home page, and Logout function |
| **4.3** | **Admin (logged in)** |
|         | Redirected to Admin page containing admin's first name once authenticated |
|         | Can only see links for Admin page, Account page, Home page, and Logout |
|         | Can only access Admin page and all its functions, Account page, Home page, and Logout function |
| **5.1** | **Account Page** |
|         | User ID, Email, Firstname, Lastname, and Phone number must be displayed |
| **5.2** | **Change Password** |
|         | A Change Password Page accessible via change password button in Account Page |
|         | Change Password Page must contain a form with current password, new password, and confirm new password data fields |
|         | Current password must match user's existing password while new password and confirm new password must be validated against requirements given in Sub-tasks 1.4 and 1.5 before the existing password is updated |
| **6.1** | **User Registration** |
|         | Date and time of registration should be stored in the database |
| **6.2** | **User Log In** |
|         | Date and time of the current log in should be stored in the database |
| **6.3** | **User Log Out** |
|         | All user logouts should be written to lottery.log (log entry must include user ID, username, and request IP) |
| **7.1** | **Lottery Draws** |
|         | Draw numbers must be encrypted using symmetric encryption before storing in the database |
| **7.2** | **Passwords** |
|         | Must be hashed before storing in the database |
| **8.1** | **Manually Entered User Draws** |
|         | Draw must contain 6 numbers when submitted |
| **9.1** | **HTTPS** |
|         | Must be implemented using a self-signed certificate |
| **9.2** | **Security Headers** |
|         | Must be added to responses sent from the application server to users' browsers |
| **10.1** | **Implemented Code** |
|         | Must be commented appropriately and sufficiently to show understanding of code |
| **10.2** | **.env File** |
|         | Must hold all application configuration data |
