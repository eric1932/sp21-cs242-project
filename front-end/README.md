# Daily Checkin - Front End

## Setup

```shell
yarn install
npm start  # open Expo
```

**Also, the API server needs to be started!**





## Abstract
### Project Purpose
This project is an automated framework that interacts with third-party websites periodically using pure HTTP requests or clicks simulation by Selenium. It can help people to complete repetitive works on the website. A common example is to receive check-in rewards from websites (e.g. Reddit daily bonus coins).

To be more specific, it can either compose HTTP requests (just like cURL) to perform actions like sign in or post an article or using Selenium to load a website and click on buttons just like a real person.

Another great feature is that it can run on cloud platforms, which means the users don't need to keep their computer open.

### Project Motivation
Many websites have daily check-in tasks. For example, some network drives say users can get more spaces if they open the websites or apps every day; some forums will automatically suspend accounts after a long period of inactivity.

I believe most of the tasks are deliberately designed by internet companies to keep a high MAU (monthly active user). To accomplish all of them, the user must visit all websites one by one and spend a huge amount of time on this, which is not very productive. This project aims to free people from such repetitive works.

## Technical Specification
- Platform:
    - Back-End: Node, Python as API server, & MongoDB; or Docker
    - Front-End: ReactNative
- Programming Languages: JavaScript & Python
- Stylistic Conventions: Airbnb JavaScript Style Guide; PEP 8
- SDK: ReactNative, FastAPI, Selenium
- IDE: WebStorm, PyCharm, and/or Visual Studio Code
- Tools/Interfaces: CLI; mobile & desktop browsers
- Target Audience: People who knows about programming

## Functional Specification
### Features
- The project has user management system to separate profiles and block unauthorized access
- User can define check-in templates for corresponding websites
    - Templates are domain-specific
    - Templates can be either in pure http requests or using Selenium (to simulate mouse clicks)
- User can instantiate templates to perform interactions using their own accounts
- The project executes all instances periodically (e.g. every 24 hours)
- The project supports persistent running
- Logs are provided to keep track of the status of each instance
- Email/push notifications can be sent to notify the user if one instance fails too many times
- Backup & Restore templates & instances
- Deploy to container
- Provide API w/ token/CMD to manage the state
- Use OCR to recognize simple verification code

### UI
- Login page
- Public templates: explore, create, and instantiate
- Private instances: update cookies; enable/disable; rename; delete

### Scope of the project
#### Limitations
- Each website has different layouts & behaviors, so writing templates needs certain skills and is still time-comsuming.
- Complicated CAPTCHAs like image recognition cannot be accomplished.
- Encrypted check-in requests cannot be made.
#### Assumptions
- Websites can be accessed with either user&pass or reusable cookies.
- Websites do not have strict validations on user interactions.
