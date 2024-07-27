# Bank Account Kata

## Description

This project is a simple bank account management system implemented using Django and Django REST Framework. It provides RESTful HTTP APIs for managing accounts, including depositing, withdrawing, transferring funds, and viewing account statements.

## Features

- **Deposit Money:** Users can deposit money into their accounts.
- **Withdraw Money:** Users can withdraw money from their accounts.
- **Transfer Money:** Users can transfer money to other accounts (IBAN accounts only).
- **View Account Statement:** Users can view their account statements, sorted by date (most recent first by default).

## Bonus Features

- **Sort Statements:** Users can sort their account statements by date in ascending or descending order.
- **Search Movements:** Users can search for movements by filtering deposits, withdrawals, and date ranges. Search results are sorted by date (most recent first by default) and can also be sorted by date in ascending or descending order.

## Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Baki100/bank_account_kata.git
    ```

2. **Navigate to the Project Directory**

    ```bash
    cd bank_account_kata
    ```

3. **Create a Virtual Environment**

    ```bash
    python -m venv env
    ```

4. **Activate the Virtual Environment**

    On Windows:

    ```bash
    env\Scripts\activate
    ```

    On macOS/Linux:

    ```bash
    source env/bin/activate
    ```

5. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

6. **Run Migrations**

    ```bash
    python manage.py migrate
    ```

7. **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

## API Endpoints

- **Deposit Money**: `POST /api/banking/deposit/`
- **Withdraw Money**: `POST /api/banking/withdraw/`
- **Transfer Money**: `POST /api/banking/transfer/`
- **View Account Statement**: `GET /api/banking/statement/`

## Tests

To run the tests:

```bash
python manage.py test
