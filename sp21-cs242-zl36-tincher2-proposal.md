# A Website Check-In Framework
Eric Liu (zl36) | Moderator: Bailey Tincher (tincher2)

## Abstract
### Project Purpose
This project is an automated framework that interacts with third-party websites periodically using pure HTTP requests or clicks simulation by Selenium. It can help people to complete repetitive works on the website. A common example is to receive check-in rewards from websites (e.g. Reddit daily bonus coins).

To be more specific, it can either compose HTTP requests (just like cURL) to perform actions like sign in or post an article or using Selenium to load a website and click on buttons just like a real person.

Another great feature is that it can run on cloud platforms, which means the users don't need to keep their computer open.

### Project Motivation
Many websites have daily check-in tasks. For example, some network drives say users can get more spaces if they open the websites or apps every day; some forums will automatically suspend accounts after a long period of inactivity.

I believe most of the tasks are deliberately designed by internet companies to keep a high MAU (monthly active user). To accomplish all of them, the user must visit all websites one by one and spend a huge amount of time on this, which is not very productive. This project aims to free people from such repetitive works.

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

## Brief Timeline
- Week 1: Set up API Server
    1. Set up FastAPI server; handle requests
    2. Set up database (possibly MongoDB)
    3. Set up Selenium
    4. Implement user management system (use token)
    5. Implement dynamic script execution with custom cookies (template engine)
- Week 2: Enable periodic tasks and persistent running
    1. Instantiate templates with start time & period
    2. Write logs
    3. Add call-back timers
    4. Ensure no leaks
- Week 3: Implement user-friendly front end; add more API entries
    1. Login page to get token
    2. Explore, create, and instantiate public templates
    3. Manage private instances: update cookies; enable/disable; rename; delete
- Week 4: Containerize with Docker & online deployment; web security
    1. Write Dockerfile
    2. Export/Import database
    3. Use HTTPS to protect the network traffic
    4. Finalize

## Rubrics
### Week 1
| Category | Total Score Allocated | Detailed Rubrics                              |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Set up FastAPI | 2 | 0: Didn't implement anything <br> 1: FastAPI listen on port `8000` <br> 2: Can handle requests like `login` and `logout` |
| Set up MongoDB | 2 | 0: None <br> 1: MongoDB running <br> 2: Can be accessed from API server
| UMS | 5 | +1 for inserting a user into database <br> +1 for successfully logging in with password <br> +2 for using a token to represent a user <br> +1 for logout & invalidate token |
| Script execution | 4 | +2 for implementing a Template class <br> +2 for executing scripts from API |
| Selenium | 2 | +2 for calling Selenium from API |
| Test line coverage | 8 | 8: 95% line coverage <br> 7: 90% line coverage <br> -1 for each 10% line coverage below 90% |
| Test design | 2 | -1: not splitting to multiple files <br> -1: missing obvious cases |

### Week 2
| Category | Total Score Allocated | Detailed Rubrics                              |
|-----------|:---------:|-------------------------------------------------------------------------------|
| API | 2 | +2: update API according to this week's changes |
| Instantiation | 4 | +1: task instantiation <br> +2: record start time & period <br> +1: store to file/database |
| Callbacks | 4 | +2: Scripts executed after certain time <br> +2: Move on to the next iteration |
| Logs | 5 | +1: output logs <br> +2: split logs for each instance <br> +2: custom log string (take return value) |
| Test line coverage | 8 | 8: 95% line coverage <br> 7: 90% line coverage <br> -1 for each 10% line coverage below 90% |
| Test design | 2 | -1: not splitting to multiple files <br> -1: missing obvious cases |


### Week 3
| Category | Total Score Allocated | Detailed Rubrics                              |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Login page | 5 | +1: see the login page <br> +2: successfully login <br> +2: get correct token |
| Template page | 5 | +1: template page design <br> +2: list public templates <br> +2: redirect to "create new instance" page |
| Instance page | 5 | +1: list instances correctly <br> +2: update instance cookies <br> +1: enable/disable instance <br> +1: rename & delete instance |
| API test cont. | 3 | +3: 6 tests for new implementations of API & others |
| React snapshot test | 4 | +4 for all 8 tests |
| Manual test | 3 | +1 for each test |


### Week 4
| Category | Total Score Allocated | Detailed Rubrics                              |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Containerization | 3 | +1: write Dockerfile <br> +2: configure all softwares in the container |
| Database import/export | 2 | +1: import database <br> +1: export database |
| Deploy online | 4 | +3: deploy to a VPS / deploy using serverless frameworks <br> +1: accessible from other devices in public network |
| HTTPS | 3 | +3: access React through HTTPS |
| CI/CD | 3 | +3: set up CI/CD in GitLab |
| Test | 5 | +2: Dockerfile build success <br> +3 for 6 other tests |
| Manual test | 5 | +1 for each test <br> test database import/export <br> test deployment <br> test HTTPS |

## Links
[Week 1](https://docs.google.com/spreadsheets/d/1f77odHr6OlwR1fM8vFNtqm_4WJKlskwQOF6iKr4ErmM/edit?usp=sharing)
[Week 2](https://docs.google.com/spreadsheets/d/1R1S59BxS3HIJLChyRrzkauHVzWEpv942RBF7mV29YBc/edit?usp=sharing)
[Week 3](https://docs.google.com/spreadsheets/d/1SAAhSzobMS2P94jIcUF4ZOF0hjmQJAhlIwrcCmXIbBU/edit?usp=sharing)
[Week 4](https://docs.google.com/spreadsheets/d/16KgyirrcJPuUFC1b4L2bL0tPvSpIacJV0MCps0lBQd0/edit?usp=sharing)
