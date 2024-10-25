# URL Shortner

URL Shortener is a lightweight web application built with Flask that allows users to shorten long URLs into easily shareable and memorable short URLs. It provides a simple API for URL shortening, retrieval of original URLs, and viewing statistics for each shortened URL.

## Features

- Shorten long URLs using custom code or random code.
- Retrieve original URLs from short codes
- View statistics such as creation date, last redirect time, and redirect count for each short URL.
- Interactive API documentation provided by Swagger UI.

## Installation

- Python 3.x or higher version is required.
- Modules required are flask, flask_swagger_ui, string, random, and datetime.
- from flask import Flask, request, jsonify
- from flask_swagger_ui import get_swagger_blueprint
- from datetime import datetime
- if the above modules are not available then you can pip install it or get a online guide to install them.

### API Endpoints

- `POST /shorten`: Shorten a URL.
- `GET /<shortcode>`: Retrieve the original URL from the short code.
- `GET /<shortcode>/stats`: Get statistics for a specific short code.

## Usage

There are 2 ways to run the code:

### First way - uisng browser

- Run the url_shortner file in the VS code terminal using the play button on top right corner.
- Open a web browser and go to `http://localhost:8080/swagger`.
- The webpage has all the documentation on how to use the application and what responses to expect.

### Second way - using curl

- open cmd or terminal.
- Naviagate to the path where you have stored the files.

  ```bash
  cd <project_directory>
  ```
- Run the flask application.

  ```bash
  python url_shortener.py
  ```
- Now open a new tab in the cmd and write cmd in the terminal and press enter.
- To access the endpoints mentioned above, use the following command by copy pasting into the cmd:

  - Creates a sorturl wiht the custome code asd123 that will redirect to original url "www.example.com".

  ```bash
  curl -X POST -H "Content-Type: application/json" -d "{\"url\" : \"https://www.example.com\",\"shortcode\" : \"asd123\"}" http://127.0.0.1:8080/shorten
  ```

  - Returns the original url that is associated with the shortcode 'asd123'.

  ```bash
  curl http://127.0.0.1:8080/asd123
  ```

  - Returrns the created date, redirect count, and last redirect of the shortcode 'asd123'

  ```bash
  curl http://127.0.0.1:8080/asd123/stats
  ```

## Testing

Unit tests are provided to ensure the functionality of the application. Make sure you are in the correct directory. To run the tests:

```bash
python -m unittest
```

- Test the status code of the response when shortening a URL, extracting a URl, and retrieving statistics.
- Test the content type of the response when shortening a URL, extracting a URl, and retrieving statistics.
- Test the data returned when shortening a URL and extracting a URL.
- Test the keys returned in the statistics data.
- Test the data types of the values returned in the statistics data.

## Limitations

### Scalability

- The current implementation stores the data in a dictionary called url_map.
- This might be okay for small projects but it might not be enough for large projects.

### Testing

- The unit tests are provided to ensure the functionality, however they could be expanded to cover more edge cases.
