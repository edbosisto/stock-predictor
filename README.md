# The Aussie Day Trader

**A personal project for practicing data analysis and web development using Flask and React frameworks.**

"The Aussie Day Trader" is a web application designed to assist stock traders, particularly day traders in Australia, by providing insights into the likely performance of specific ASX stocks based on the previous day's US Index performance. The app leverages data analysis techniques to offer predictions for the performance of selected stocks the following day, once the US market has closed.

## Features

- Real-time updates of the S&P 500 index and ASX stock data.
- Comparative analysis of ASX stocks with the previous day's S&P 500 performance.
- Easy-to-use interface for selecting ASX stocks and viewing analysis results.

## Table of Contents

- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Backend Setup

1. Clone this repository to your local machine.
2. Navigate to the `backend` directory:
  cd backend
3. Set up a virtual environment (optional but recommended):
  python -m venv venv
4. Activate the virtual environment:

   - On Windows:
     venv\Scripts\activate
   - On macOS and Linux:
     source venv/bin/activate
5. Install the required Python packages:
  pip install -r requirements.txt
6. Set up a MySQL database and configure the necessary environment variables (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) in a `.env` file based on the provided `.env.example`.
7. Download and prepare stock data from Yahoo Finance.
8. Run the Flask backend server:
   python app.py

### Frontend Setup

1. Navigate to the `frontend` directory:
   cd frontend
2. Install Node.js and npm if not already installed.
3. Install the required Node.js packages:
   npm install
4. Start the React development server:
   npm start
The app will be accessible at `http://localhost:3000` in your web browser.

## Usage

1. Open the app in your web browser.

2. Explore the real-time updates of the S&P 500 index on the left and choose an ASX stock from the dropdown menu on the right.

3. View the current market values of the selected ASX stock and its analysis based on the previous day's S&P 500 performance.

## Contributing

Contributions are welcome! If you find a bug or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License (see [LICENSE](LICENSE)).
