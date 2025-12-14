# Fitplan-Hub

# Overview

    FitPlanHub is a backendd service built using Django REST Framework that powers a fitness platform where certified trainers create fitness plans and users can discover, purchase, and follow these plans.
    The backend focuses on clean authentication, role-based access, and simple business logic without overcomplicating the system.

    This project was developed as part of an assignment and follows real-world backend design practices.

    Tech Stack

        Python

        Django

        Django REST Framework

        PostgreSQL

        JWT Authentication (SimpleJWT)

# Core Features
    Authentication

        Signup and login for both users and trainers

        Email-based authentication

    Trainer Functionality

        Trainers can create fitness plans

        Update or delete only their own plans

        Each plan contains title, description, price, and duration

    User Functionality

        Users can view all available plans 

        Subscribe to a fitness plann

    Access Control

    Only subscribed users can view full plan details
