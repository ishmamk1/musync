# Musync

Musync is a web application that utilizes the Spotify API to provide users with personalized music recommendations, display their past tracks and favorite artists, and create playlists based on their preferences.

## Features

- **Authentication:** Users can log in to their Spotify account securely using OAuth authentication.
- **Top Artists and Tracks:** The application displays the user's top artists and tracks, providing insights into their musical preferences.
- **Recently Played:** Users can view their recently played tracks, including details such as title, artist, album, and image.
- **Playlist Generation:** Musync generates playlists based on user input, including artist name and genre preferences. Users can create and save personalized playlists directly to their Spotify account.
- **Error Handling:** The application gracefully handles errors and provides users with helpful error messages when encountering issues.

## Technologies Used

Musync is built using the following technologies:

- **Python:** The backend logic of the application is written in Python, utilizing Flask as the web framework.
- **HTML/CSS:** The frontend user interface is designed using HTML and styled with CSS.
- **JavaScript:** Some frontend interactions and dynamic content are implemented using JavaScript.
- **Spotipy:** Spotipy is a lightweight Python library for the Spotify Web API, enabling seamless integration with Spotify services.
- **OAuth:** The application uses OAuth authentication to securely authenticate users with their Spotify accounts.

## Getting Started

To run Musync locally, follow these steps:

1. Open your terminal or command prompt.

2. Use the `git clone` command followed by the repository URL:

   ```bash
   git clone https://github.com/ishmamk1/musync.git
   ```
3. In your terminal run:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a Spotify developer account and change the `CLIENT_ID` and `CLIENT_SECRET` to its respective values.

6. Run the command:
   ```bash
   python main.py
   ```

## Visuals of Musync

- Landing Page
  
  <img width="1440" alt="Screenshot 2024-03-18 at 5 27 25 PM" src="https://github.com/ishmamk1/musync/assets/117555551/cfde6447-f67e-4dc6-8fc0-34a4f54cf931">

- Home Page Once User is Authenticated

<img width="1440" alt="Screenshot 2024-03-18 at 5 27 36 PM" src="https://github.com/ishmamk1/musync/assets/117555551/cccd5356-824f-4fb9-92eb-feb3994a1c12">

-Recently Played Tracks

<img width="1440" alt="Screenshot 2024-03-18 at 5 27 42 PM" src="https://github.com/ishmamk1/musync/assets/117555551/11bca7d1-6f6d-42c7-be67-4dca0c5b75d0">

-Recieve Recommendations & Create Playlist Page

<img width="1440" alt="Screenshot 2024-03-18 at 5 28 34 PM" src="https://github.com/ishmamk1/musync/assets/117555551/b88b6531-c14f-4a82-99a9-7eccd015cac3">

-Confirmation Of Working Product

<img width="1432" alt="Screenshot 2024-03-18 at 5 29 31 PM" src="https://github.com/ishmamk1/musync/assets/117555551/e33ffaf1-72a7-4469-aef3-f969ba733dab">



  
