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
- Week 3: Implement user-friendly front end; focus on desktop browsers; add more API entries
    1. Login page to get token
    2. Explore, create, and instantiate public templates
    3. Manage private instances: update cookies; enable/disable; rename; delete
- Week 4: Adapt front-end for mobile devices; online deployment; web security
    1. build native apps
    2. iOS push notifications
    3. Write Dockerfile
    4. Export/Import database
    5. Use HTTPS to protect the network traffic
    6. Finalize

## Rubrics
### Week 1
| Category | Total Score Allocated | Detailed Rubrics                              |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Set up FastAPI | 1 | 0: Didn't implement anything <br> 1: FastAPI listen on port `8000` and can handle requests like `login` and `logout` |
| Set up MongoDB | 1 | 0: None <br> 1: MongoDB can be accessed from API server |
| UMS | 5 | +1 for inserting a user into database <br> +1 for successfully logging in with password <br> +2 for using a token to represent a user <br> +1 for logout & invalidate token |
| Script execution | 4 | +2 for implementing a Template class <br> +2 for executing scripts from API |
| pylint | 2 | +1 for using pylint and appropriate rules <br> +1 if score >= 0.9 |
| Selenium | 2 | +1 for connecting WebDriver in filesystem and Selenium in python <br> +1 for using Selenium to retrieve today's logo of Google (warmup for next week's content) |
| Test line coverage | 8 | 8: 95% line coverage <br> 7: 90% line coverage <br> -1 for each 10% line coverage below 90% |
| Test design | 2 | -1: not splitting to multiple files <br> -1: missing obvious cases |

### Week 2
| Category | Total Score Allocated | Detailed Rubrics                              |
|-----------|:---------:|-------------------------------------------------------------------------------|
| API | 2 | +1: implement login API <br> +1: implement script execution API that calls Selenium |
| Instantiation | 4 | +1: task instantiation <br> +2: record start time & period <br> +1: store to file/database |
| Callbacks | 4 | +2: Scripts executed after certain time <br> +2: Move on to the next iteration |
| Logs | 5 | +1: output logs <br> +2: split logs for each instance <br> +2: custom log string (take return value of the `exec` function as the log message) |
| Test line coverage | 8 | 8: 95% line coverage <br> 7: 90% line coverage <br> -1 for each 10% line coverage below 90% |
| Test design | 2 | -1: not splitting to multiple files <br> -1: missing obvious cases |


### Week 3
| Category | Total Score Allocated | Detailed Rubrics                              |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Login page | 5 | +1: see the login page <br> +2: successfully login <br> +2: get correct token |
| Template page | 5 | +1: template page design <br> +2: list public templates <br> +2: redirect to "create new instance" page |
| Instance page | 5 | +1: list instances correctly <br> +2: update instance cookies <br> +1: enable/disable instance <br> +1: rename & delete instance |
| API test cont. | 3 | +3: 6 tests for new implementations of API & others |
| snapshot test | 4 | +3 for 6 normal tests <br> +1 for 2 mock tests |
| Documentation | 2 | +2: writing good documentation about the front-end |
| ESLint | 1 | +1: using strict ESLint rules |


### Week 4
| Category | Total Score Allocated | Detailed Rubrics                              |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Public deployment | 2 | +2: access the website through the Internet |
| Mobile port (iOS) | 7 | +2: mobile UI <br> +1: register push notification service <br> +2: send notifications when success and/or fail <br> +2: sideload .ipa |
| Database import/export | 4 | +1: import database <br> +3: automated database backup |
| CI/CD | 2 | +1: Auto lint/test <br> +1: auto-deployment |
| Test | 6 | +1: manual notification test <br> +1: stress test <br> +2: error handling when the database is down <br> +2: error handling when the API server is down |
| Documentation | 4 | +2: write documentation that helps others to download & set up the project <br> +2: create a website for documentation using tools like Docusaurus or GitHub pages |

## Links
[Week 1](https://docs.google.com/spreadsheets/d/1f77odHr6OlwR1fM8vFNtqm_4WJKlskwQOF6iKr4ErmM/edit?usp=sharing)

[Week 2](https://docs.google.com/spreadsheets/d/1R1S59BxS3HIJLChyRrzkauHVzWEpv942RBF7mV29YBc/edit?usp=sharing)

[Week 3](https://docs.google.com/spreadsheets/d/1SAAhSzobMS2P94jIcUF4ZOF0hjmQJAhlIwrcCmXIbBU/edit?usp=sharing)

[Week 4](https://docs.google.com/spreadsheets/d/16KgyirrcJPuUFC1b4L2bL0tPvSpIacJV0MCps0lBQd0/edit?usp=sharing)
