# Trade2goal

# Overview

This project is a web server implemented using Django, featuring functionalities such as chat, account management, post management, and team information. It is characterized by user authentication through Firebase, real-time chat using Django Channels, scheduled news crawling with Celery, and secured communication with HTTPS.

# Technology Stack

- Django
- Django Channels
- Celery
- Firebase Authentication
- Nginx
- Gunicorn
- Daphne
- AWS EC2
<img width="833" alt="image" src="https://github.com/footballStock/server/assets/64965613/8dc5ca20-2908-45a4-bb4b-2626e8e5f1bc">


# Key Features

## 1. Accounts

The `Accounts` app in this project is integrated with Firebase Authentication, providing a secure and scalable solution for managing user authentication. This setup allows the application to offload the complex responsibilities of securely handling user logins and token verification to Firebase.

### Integration in `settings.py`

The Django project's `settings.py` file is configured to integrate Firebase Authentication as follows:

1. **Firebase Project Configuration**: The Firebase project's configuration is defined, including `API_KEY`, `AUTH_DOMAIN`, `DATABASE_URL`, `PROJECT_ID`, `STORAGE_BUCKET`, `MESSAGING_SENDER_ID`, and `APP_ID`. These values are sourced from the Firebase project settings.

2. **Authentication Backend**: The custom authentication backend `FirebaseAuthentication` is specified in the `AUTHENTICATION_BACKENDS` setting, enabling Django to use Firebase for user authentication.

3. **Firebase SDK Initialization**: Firebase Admin SDK is initialized in `settings.py` using the Firebase project configuration. This setup is essential for verifying ID tokens sent by the client side.

### Firebase Authentication in `authentication.py`

The core of Firebase Authentication is implemented in `authentication.py` within the `accounts` app. Key components of this implementation include:

- **FirebaseAuthentication Class**: This custom authentication class extends Django’s base authentication module, overriding the `authenticate` method to handle token verification through Firebase.

- **Token Verification**: When a request is made to the server, the `FirebaseAuthentication` class extracts the ID token from the request's authorization header. It then uses the Firebase Admin SDK to verify the token’s validity.

- **User Retrieval or Creation**: Once the token is verified, the class attempts to retrieve the corresponding user from the Django database. If the user does not exist, it creates a new user record.

- **Integration with Django's User Model**: This authentication system is seamlessly integrated with Django's built-in User model, ensuring that it works well with other Django apps and functionalities that depend on user authentication.

This approach to authentication leverages Firebase’s robust security features and provides a seamless authentication experience, all while integrating smoothly with Django’s user management system.

## 2. Chat Feature

The Chat feature in this project is built using Django Channels, providing real-time communication capabilities. This feature is primarily configured in `router.py` and `consumers.py`, enabling WebSocket connections for real-time messaging.

### Router Configuration (`router.py`)

The `router.py` file defines the routing of WebSocket requests to the appropriate consumer based on the URL pattern. This is crucial for directing incoming WebSocket connections to the correct consumer for handling:

```python
# Example from router.py
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    # WebSocket chat handler
    "websocket": URLRouter(
        chat.routing.websocket_urlpatterns
    )
})
```

### Chat Consumer (consumers.py)

The `consumers.py` file contains the `ChatConsumer` class, which manages WebSocket connections for the chat functionality. Key aspects include:

- **WebSocket Connection Management**: Methods to handle connecting and disconnecting WebSocket clients.

- **Message Handling**: Methods to receive messages from the client and send messages back to the client or broadcast them to a group.

- **Group Management**: Using Django Channels' group system to manage real-time communication among multiple clients.

```python
# Example from consumers.py
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Method to handle connection
        ...

    def disconnect(self, close_code):
        # Method to handle disconnection
        ...

    def receive(self, text_data):
        # Method to handle receiving a message
        ...

    def chat_message(self, event):
        # Method to handle sending a message
        ...
```

This setup enables the application to handle multiple users in a chat room, facilitating real-time communication among them. The combination of Django Channels' routing and consumer mechanism provides a robust foundation for building real-time chat applications.

## 3. Post Feature

The `Post` feature is implemented using Django's `ModelViewSet`, providing a comprehensive set of view behaviors for the `Post` model. Here's an overview of the `PostViewSet` and its key functionalities:

### `PostViewSet` Overview

`PostViewSet` extends `viewsets.ModelViewSet`, offering CRUD operations and more on the `Post` model. It defines various actions like list, retrieve, create, update, destroy, like, and dislike, with specific permission classes for each action.

### Key Functionalities

1. **List Posts (`list`)**: Retrieves and lists all posts, ordered by creation date in descending order. Pagination is implemented to display a limited number of posts per page.

2. **Retrieve Post (`retrieve`)**: Fetches a single post based on its ID. The method also checks if the current user has liked or disliked the post, adding this information to the response.

3. **Top 3 Posts (`top3post`)**: Returns the top 3 posts with the highest number of likes.

4. **Create Post (`create`)**: Allows authenticated users to create a new post. The post's author is automatically set to the current user.

5. **Update Post (`update`)**: Enables the author of a post to update it. If the user attempting the update is not the author, a permission denied error is raised.

6. **Delete Post (`destroy`)**: Allows the author to delete their post. Similar to update, it checks if the current user is the author.

7. **Like a Post (`like`)**: Enables authenticated users to like a post. If the post is already liked by the user, the like is removed. If the post is disliked, the dislike is removed upon liking.

8. **Dislike a Post (`dislike`)**: Allows users to dislike a post. Similar to like, if the post is already disliked, the dislike is removed. If the post is liked, the like is removed upon disliking.

### Model and Serializer

- The `Post` model includes fields like title, content, image, author, etc.
- `PostSerializer` is used to serialize and deserialize `Post` instances. It includes custom fields and methods to handle likes and dislikes counts.

### Permissions

- Actions like create, update, and destroy require the user to be authenticated (`IsAuthenticated`).
- Actions like list and retrieve are available to any user (`AllowAny`).

This setup provides a comprehensive and interactive platform for users to engage with posts, offering a mix of social media-like functionalities such as liking and disliking posts, along with standard CRUD operations.

## 4. Team Info Feature

The `Team Info` feature in this project focuses on providing detailed information about various sports teams. A significant part of this functionality includes the implementation of a news crawling scheduler using Celery.

### Overview

`Team Info` offers a comprehensive set of models and views that handle the storage and retrieval of data related to sports teams. This includes information about team history, players, match records, and more.

### Celery for News Crawling

One of the key functionalities in the `Team Info` app is the automated news crawling scheduler, which is implemented using Celery. This scheduler periodically crawls news sources for the latest updates related to the teams and stores them in the database.

#### Celery Configuration and Task Setup

- Celery is configured with Django settings and connected to a message broker (like Redis or RabbitMQ) for task management.
- A custom Celery task named `get_news` is defined to handle the news crawling process.
- The Celery Beat scheduler is set up to run this task periodically (e.g., every hour), ensuring that the news data is regularly updated.

### Models and Views

- The app includes models like `Team`, `Player`, `Match`, `News`, etc., each storing specific information about sports teams and related entities.
- Views are set up to provide access to this data through RESTful APIs or Django templates, depending on the project's architecture.

### Integration with Django REST Framework

- For projects leveraging Django REST Framework, serializers are defined for each model to facilitate JSON serialization and deserialization.
- ViewSets and Routers are used to create endpoints for CRUD operations and other custom actions related to team information.

This `Team Info` feature, combined with the Celery-based news crawling scheduler, provides a dynamic and up-to-date repository of information about sports teams, making it an essential part of the project for sports enthusiasts and analysts.

# Deployment

The application is deployed on an Amazon Web Services (AWS) EC2 instance, utilizing Nginx, Gunicorn, and Daphne for web server setup. The deployment uses a subdomain approach for HTTPS, with the subdomain `api.trade2goal.com`, and SSL certificates obtained from Let's Encrypt.

### AWS EC2 Instance

- **EC2 Setup**: Hosted on an AWS EC2 instance, the application benefits from AWS's scalable cloud computing capacity. The instance is tailored with adequate resources to manage the application's load.
- **Security Configuration**: Security groups are set up to regulate traffic, ensuring only necessary ports are accessible for secure and efficient operation.

### Web Server Configuration

- **Nginx**: Serving as a reverse proxy, Nginx handles incoming HTTP requests, directing them to Gunicorn or Daphne. It's configured to optimize performance and manage secure connections.
- **Gunicorn**: This Python WSGI HTTP Server interfaces with the Django application, managing and running the Python code in a production setting.
- **Daphne**: As an interface server for ASGI applications, Daphne handles WebSocket requests, crucial for the real-time features of the application.

### Subdomain and HTTPS Configuration

- **Subdomain**: The application uses the subdomain `api.trade2goal.com`. This dedicated subdomain aids in structuring and organizing the web services, particularly for handling API requests separately.
- **SSL Certificates**: SSL certificates are obtained from [Let's Encrypt](https://letsencrypt.org/), a widely-trusted certificate authority. These certificates encrypt data transmitted between the server and clients, ensuring secure communication over the internet.

This deployment strategy, combining AWS's robust cloud infrastructure with efficient web server configuration and secure HTTPS setup, ensures reliable, scalable, and secure access to the application.

## Installation

Follow these step-by-step instructions to set up the project environment and install necessary dependencies.

### Setting Up a Virtual Environment

1.  **Create a Virtual Environment**: First, create a virtual environment to isolate the project dependencies. Run the following command in your terminal:

    ```bash
    python -m venv myenv
    ```

    Replace `myenv` with your desired environment name.

2.  **Activate the Virtual Environment**:

    - On Windows, activate the environment using:

    ```bash
    myenv\Scripts\activate
    ```

    - On macOS or Linux, use:

    ```bash
    source myenv/bin/activate
    ```

### Installing Dependencies

Once the virtual environment is activated, install the project dependencies:

```bash
pip install -r requirements.txt
```

This command will install all the required packages listed in the requirements.txt file.

# Usage

After successfully installing the project, you can test and run it locally.

1. Migrate the Database:

- **Before running the server, make sure to apply the migrations**:

  ```bash
  python manage.py migrate
  ```

2. Run the Server:

- **Start the Django development server**:

  ```bash
  python manage.py runserver
  ```

3. Access the Application:

   The server will start running on `http://127.0.0.1:8000/`. Open this URL in your web browser to interact with the application.

### Testing the Application

- Navigate through the application to test different functionalities.
- Use the admin panel at `http://127.0.0.1:8000/admin/` to manage the application (you may need to create a superuser first).
- Test the API endpoints using tools like Postman or through the browser, if applicable.

Follow these steps to install and use the project on your local machine. The project is now set up and ready for further development and testing.
