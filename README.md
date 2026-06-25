Host machine information

OS Name:                       Microsoft Windows 11 Home Single Language
OS Version:                    10.0.26200 N/A Build 26200
OS Manufacturer:               Microsoft Corporation
OS Configuration:              Standalone Workstation
OS Build Type:                 Multiprocessor Free
Registered Owner:              Lenovo

System Manufacturer:           LENOVO
System Model:                  82WQ
System Type:                   x64-based PC
Processor(s):                  1 Processor(s) Installed.
                               [01]: Intel64 Family 6 Model 183 Stepping 1 GenuineIntel ~2200 Mhz

Virtualization software and version

Oracle VirtualBox
VirtualBox Graphical User Interface
Version 7.2.2 r170484 (Qt6.8.0 on windows)
Copyright © 2025 Oracle and/or its affiliates


# Food Store / Culinary Connect

This repository contains a food discovery application that uses Spoonacular for recipe data and Flask for authentication.

- `backend/` Flask backend with SQLite and user authentication.
- `culinaryconnect/` React frontend with login modal, Spoonacular search, routes, and recipe UI.

## Features

- Flask + SQLAlchemy backend using SQLite
- Secure bcrypt password hashing for user authentication
- Login API (`POST /api/login`)
- React login modal and welcome page
- Frontend recipe search and recipe detail views powered by Spoonacular

## Project structure

- `backend/`
  - `app.py` application factory and blueprint registration
  - `models.py` SQLAlchemy `User` model
  - `auth/` authentication blueprint
  - `seed.py` seed script to populate SQLite and create 500 users
- `culinaryconnect/`
  - React app with proxy to backend
  - `src/components` reusable UI components
  - `src/pages` page-level views and routes

## Getting started

### Backend setup

1. Change to the backend directory:

```bash
cd backend
```

2. Install dependencies using Pipenv:

```bash
pipenv install
```

3. Seed the database with test users:

```bash
pipenv run python seed.py
```

4. Start the backend server:

```bash
pipenv run python app.py
```

The backend will run on `http://127.0.0.1:5000`.

### Frontend setup

1. Change to the frontend directory:

```bash
cd culinaryconnect
```

2. Install dependencies:

```bash
npm install
```

3. Start the React app:

```bash
npm start
```

The React app should run on `http://localhost:3000` and proxy API requests to the backend.

## API Endpoints

- `POST /api/login` : login with JSON payload `{ "username": "<username>", "password": "<password>" }`
- Recipe browse and search happen through the Spoonacular API from the frontend

## Notes

- Passwords are stored hashed with bcrypt and never persisted in plaintext.
- For local testing, the seed script generates 500 unique users and writes `users.csv` with plaintext passwords for one-time test lookup.
