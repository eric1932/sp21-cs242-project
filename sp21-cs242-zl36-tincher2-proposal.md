# A Website Check-In Framework
Eric Liu (zl36) | Moderator: Bailey Tincher (tincher2)

## Abstract
### Project Purpose
This is an automated framework that *interacts* with third-party websites and receives check-in rewards every day on behalf of the user.

### Project Motivation
I believe most daily check-in tasks are designed by internet companies to maintain MAU (monthly active user). To receive all awards every day, the user must visit all of the websites and spend a huge amount of time on this, which is not very productive. This project aims to free people from such repetitive works.

e.g. Reddit daily bonus

![](./Reddit.png)

## Technical Specification
- Platform: 
    - Back-End: Node, Python as API server, & MongoDB; or Docker
    - Front-End: React
- Programming Languages: JavaScript & Python
- Stylistic Conventions: Airbnb JavaScript Style Guide; PEP 8
- SDK: React, FastAPI, Selenium
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

### Scope of the project
#### Limitations
- Each website has different layouts & behaviors, so writing templates needs certain skills and is still time-comsuming.
- Complicated CAPTCHAs like image recognition cannot be accomplished.
- Encrypted check-in requests cannot be made.
#### Assumptions
- Websites can be accessed with either user&pass or reusable cookies.
- Websites do not have strict validations on user interactions.

## Brief Timeline
- Week 1: Set up API Server
    1. Set up FastAPI server; handle requests
    2. Set up database (possibly MongoDB)
    3. Implement user management system (use token)
    4. Implement dynamic script execution with custom cookies (template engine)
- Week 2: Enable periodic tasks and persistent running
    1. Instantiate templates with start time & period
    2. Write logs
    3. Add call-back timers
    4. Ensure no leaks
- Week 3: Implement user-friendly front end; add more API entries
    1. Login page to get token
    2. Explore, create, and instantiate public templates
    3. Manage private instances: update cookies; enable/disable; rename; delete
- Week 4: Containerize with Docker & online deployment
    1. Write Dockerfile
    2. Export/Import database

## Rubrics
### Week 1
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
|  Function a |  4  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed function a |
|  Function b |  2  |  0: Didn't implement anything <br> 1: implemented ... <br> 2: completed function b |
|  Function c |  4  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed function c |
|  Function d |  5  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 5: completed function d |
|  Test a |  6  |  0: Didn't implement tests <br> 1: implemented ... <br> 3: implemented .... <br> 6: completed test a |
|  Test b |  4  |  0: Didn't implement tests <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed test b |

### Week 2
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
|  Function a |  4  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed function a |
|  Function b |  2  |  0: Didn't implement anything <br> 1: implemented ... <br> 2: completed function b |
|  Function c |  4  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed function c |
|  Function d |  5  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 5: completed function d |
|  Test a |  6  |  0: Didn't implement tests <br> 1: implemented ... <br> 3: implemented .... <br> 6: completed test a |
|  Test b |  4  |  0: Didn't implement tests <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed test b |


### Week 3
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
|  Function a |  4  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed function a |
|  Function b |  2  |  0: Didn't implement anything <br> 1: implemented ... <br> 2: completed function b |
|  Function c |  4  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed function c |
|  Function d |  5  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 5: completed function d |
|  Test a |  6  |  0: Didn't implement tests <br> 1: implemented ... <br> 3: implemented .... <br> 6: completed test a |
|  Test b |  4  |  0: Didn't implement tests <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed test b |


### Week 4
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
|  Function a |  4  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed function a |
|  Function b |  2  |  0: Didn't implement anything <br> 1: implemented ... <br> 2: completed function b |
|  Function c |  4  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed function c |
|  Function d |  5  |  0: Didn't implement anything <br> 1: implemented ... <br> 3: implemented .... <br> 5: completed function d |
|  Test a |  6  |  0: Didn't implement tests <br> 1: implemented ... <br> 3: implemented .... <br> 6: completed test a |
|  Test b |  4  |  0: Didn't implement tests <br> 1: implemented ... <br> 3: implemented .... <br> 4: completed test b |
