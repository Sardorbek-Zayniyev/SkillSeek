# SkillSeek

**SkillSeek** is a Full-Stack web platform designed for developers to enhance their skills through collaborative learning. The platform enables users to interact with each other, contribute to open-source projects, share resources, and track their progress across various technologies.

## Features
- **User Profiles**: Create and manage personalized profiles to display your skills and achievements.
- **Messaging**: Send and receive messages between users for collaboration.
- **Reviewing**: Leave and receive feedback on projects and contributions.
- **Voting**: Upvote or downvote projects and resources to highlight the best ones.
- **Project Contributions**: Browse open-source projects and contribute by submitting code, issues, or suggestions.
- **Learning Resources**: Upload and share tutorials, guides, and other educational materials.
- **Notifications**: Stay updated with project activity, messages, and comments.
- **API Development**: Access backend APIs to interact with the system programmatically.

## Technologies Used

- **Django**: Backend web framework.
- **Django REST Framework**: For building APIs.
- **PostgreSQL**: Database management.
- **JWT**: JSON Web Token authentication for secure login.
- **Whitenoise**: To serve static files in production.
- **asgiRef**: For asynchronous support in Django.
- **PyJWT**: For working with JSON Web Tokens.
- **Pillow**: Image processing.
- **psycopg2**: PostgreSQL database adapter.
- **python-decouple**: For handling environment variables.
- **black**: Code formatting.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Sardorbek-Zayniyev/SkillSeek.git
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run migrations:
    ```bash
    python manage.py migrate
    ```

4. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Contributing

Feel free to fork the repository and submit pull requests to contribute to the project. We are open to all kinds of improvements, including bug fixes, feature additions, and documentation improvements.


## Contact

For any issues or feedback, please open an issue on this repository.
