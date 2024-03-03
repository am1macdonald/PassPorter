# Pass Porter

Pass Porter is an Authentication Platform built with Python, SQL, JavaScript, and NPM.

## Installation

Provide instructions on how to install your project. For example:

1. Clone the repository:
    ```
    git clone https://github.com/username/repository.git
    ```

2. Navigate to the project directory:
    ```
    cd repository
    ```

3. Install the required node dependencies:
    ```
    npm install
    ```
4. Set up virtual environment:
    ```
    python3 -m venv venv
    ```
5. Activate virtual environment:
    ```
    source venv/bin/activate
    ```
6. Install the required python dependencies:
    ```
    pip install -r requirements.txt
   ```
7. Create a `.env` file in the root of the project using the `.env.example` file as a template.
   - I used `openssl rand -base64 60` in my Linux shell

## Usage

Intended for educational purposes only. This project is not intended for production use.

To use Pass Porter, it might be best to run on a server behind a reverse proxy.

I haven't done this yet, but I plan to use Nginx as a reverse proxy for this project.

## Roadmap / Wishlist

- [x] Create a basic authentication system
- [x] Add a database to store user information
- [x] Add a way to reset passwords
- [x] Add a way to verify email addresses
- [ ] Build emailer to deliver verification links
- [x] Add a way to manage user sessions using JWT
- [x] Add authorization endpoint
- [ ] Add a get token endpoint
- [ ] Transition from HS256 to RS256 for JWT encoding

## Contributing

If you would like to contribute to this project, please open an issue or a pull request.

I won't be accepting any pull requests into this project but depending on interest, I might create a fork of this
project and accept pull requests there.

## Authors and Acknowledgment

Me, myself, and I.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

My GitHub username is `@am1macdonald`. You can find me at

## Project Status

This project is currently in development.
