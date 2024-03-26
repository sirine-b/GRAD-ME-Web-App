# COMP0034 Coursework 2 (2023/24)
## OVERVIEW
The GRAD:ME! web app is a dashboard built with Dash in order to enable its users (final-year unversity students) to visualise data related to employment prospects for various courses and study modes.

This dashboard enables the students to selects their course, study mode (Full-Time or Part-Time), kis level (3 or 4) and their countries of interests within the UK and view data regarding the expected salaries, graduates' satisfaction rate and much more!

## INSTALLATION and EXECUTION
### 1. Clone repository
Clone the repository to your virtual IDE
- If you are using VSCode, you can select the Clone Repository button in the Source Control view and copy and paste this link to the repository in the search bar: https://github.com/ucl-comp0035/comp0034-cw2i-sirine-b.git.
- If you are using PyCharm, see https://www.jetbrains.com/help/pycharm/manage-projects-hosted-on-github.html.

### 2. Create and activate a virtual environment in the project folder

MacOS: 
```bash 
python3 -m venv .venv
source .venv/bin/activate
```
Windows: 
```bash
py -m venv .venv
.venv\Scripts\activate
``` 
### 3. Installations
#### a. Install latest version of pip
```bash
pip install --upgrade pip
```
#### b. Install Dependencies
To install the dependencies required to run this REST API, enter the following command in your IDE terminal:
```bash
pip install -r requirements.txt
```
#### c. Install the GRAD:ME! Dash app code
```bash
pip install -e .
```

### 3. Run the Application
- Run the application with the command:
```bash
python src/app.py --debug
```
- Open a browser and go to http://127.0.0.1:5000 

- To stop the app, press : `CTRL+C`

## TESTING

### 1. Through GitHub Actions (Continuous Integration)
All the tests were ran through Github actions as that is what worked best for me. To do so, simply:

#### a. Make sure the dash_app.yml file exists within the .github/workflows folder

#### b. Commit and sync any changes made locally onto your main branch on GitHub

***Pycharm***:
Go to VCS > Git > Commit File . Click on Commit File Button. Write your commit message and click on **Commit**
Then, to push the changes onto GitHub: Go to VCS > Git > Push

***VSCode***:
Go to the Source Control (or Ctrl+Shift+G) tab. Write your commit message and click on **Commit** and then **Sync**

#### c. Check latest workflow run to view test results and coverage report
Go to your GitHub repository for this app. Click on the **Actions** tab at the top of the page. Open the last workflow run.


### 2. Locally
However, if you would like to try to run the tests and obtain the coverage reports locally, you can follow these next steps:

#### a. Running the Tests

To run the tests, execute the following command:

```bash
pytest -v
```
#### b. Test Coverage

Run the tests with coverage:

```bash
coverage run -m pytest tests/test_dash_app.py
```
Obtain the coverage report: 

```bash
coverage report -m
```
