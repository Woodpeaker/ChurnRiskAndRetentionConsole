# Churn Risk and Retention Console Application



Simple React frontend for ChurnRiskAndRetentionConsole.

## Set up

Make sure Python 3.8+ and Node.js are installed on your system.

Using powershell, cd into the project directory and run the following commands to set up the backend and frontend:

Steps to start backend (powershell):
- python -m Backend.App.main

Steps to start frontend (powershell):
- cd Frontend
- npm start

The dev server proxies API requests to http://localhost:5000 (Flask backend).

## How to use the application

As a client, to use this application, when you access the page you can view the list of customers and their churn risk scores. You can sort the customers based on the columns showned, and navigate through the paginated results. The application provides a simple and intuitive interface for managing customer data and understanding churn risk.
When you click on a customer, you can view detailed information about that customer, including their profile, transaction history, and support tickets. This allows you to gain insights into the customer's interactions with the company and identify potential areas for improvement. To change the outreach status of a customer, you can click on the "Change Outreach Status" button and select the desired status from the dropdown menu. This allows you to update the customer's status and track their engagement with the company. You get to see all the rules for how the risk score is calculated on the homepage, which provides transparency and helps you understand how the scores are derived.

## Design decisions

I choose Flask as the backend framework because it is lightweight, easy to set up, and has a simple routing system. Flask is also well-suited for building RESTful APIs, which makes it a good choice for this application. Additionally, Flask has a large community and extensive documentation, which makes it easier to find solutions to any issues that may arise during development.
The frontend is built using React, which is a popular JavaScript library for building user interfaces. React allows for the creation of reusable components, making it easier to manage and maintain the codebase. It also has a large ecosystem of libraries and tools that can be used to enhance the development process.

The data modeling for this application is based on a relational database structure, which allows for efficient storage and retrieval of customer data. The models structure is designed to capture relevant information about customers, their interactions with the company, and their churn risk. This includes tables for customer profiles, transaction history, support tickets, and churn risk scores.

How I tackle the pagination and filtering of the data in the frontend is by implementing a combination of server-side and client-side techniques. On the server-side, I use query parameters to handle pagination and filtering requests. The backend API endpoints accept parameters such as page number, page size, and filter criteria (e.g., customer status, churn risk level) to return the appropriate subset of data. Howerver, the client side does not have the filtering functionality implemented yet.

For the error handling and logging, I implement a centralized error handling mechanism in the backend using Flask's error handlers. This allows me to catch and respond to different types of errors consistently. I also use Python's built-in logging module to log important events, errors, and debug information to a log file for later analysis.

## Trade-offs and shortcuts

The trade-offs I made in the design and implementation of this application include choosing Flask over more feature-rich frameworks like Django, which may have provided more built-in functionality but would have added complexity. Additionally, I focused on building a straightforward frontend with React, prioritizing ease of use and maintainability over advanced UI features. I've also group all routes in a single file for simplicity, but this could lead to scalability issues as the application grows. In the future, I may consider refactoring the routes into separate modules to improve maintainability. The scoring algorithm is designed to be simple and easy to understand, but it may not capture all the nuances of customer behavior.

For shortcuts I used copilot to generate boilerplate code for the frontend components and backend routes, which helped speed up development. However, I made sure to review and modify the generated code to fit the specific requirements of the application. The main logic and functionality were implemented manually to ensure that the application meets the desired specifications and performance standards.

With more time and resources, I would consider implementing additional features such as user authentication and authorization, more advanced data visualization components, and integration with external services for enhanced customer insights. I would also explore optimizing the performance of the application by implementing caching strategies and improving database query efficiency. Additionally, I would invest in writing comprehensive unit and integration tests to ensure the reliability and stability of the application over time. I will improve the risk scoring algorithm by extending more scoring criteria and breakdown of the risk score to provide more actionable insights for the business.