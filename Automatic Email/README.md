# Automatic Email System

## Overview

This project is an **Automatic Email System** built using Object-Oriented Programming (OOP) principles in Python. The system allows users to automate sending customized emails, making it useful for businesses, marketing, and personal use cases where bulk or personalized email sending is required.

## Project Structure

The project is organized as follows:

Automatic-Email/ ├── README.md # Project overview and instructions ├── email_sender.py # Main script for sending emails ├── config.py # Configuration file with user settings (SMTP server, login credentials) ├── templates/ # Folder with email templates for personalization │ ├── welcome_template.txt # Example welcome email template │ └── followup_template.txt # Example follow-up email template ├── data/ # Folder with recipient information │ └── recipients.csv # CSV file with recipient names, emails, and other details └── requirements.txt # List of dependencies


## Features

- **Automated Email Sending**: Automatically sends emails based on the template and recipient information.
- **Personalization**: Uses placeholders in templates to personalize each email.
- **Configurable SMTP Settings**: Supports different SMTP servers and allows secure login configuration.
- **CSV-based Recipients List**: Loads recipient data from a CSV file for easy management.