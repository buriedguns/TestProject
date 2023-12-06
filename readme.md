### Tests installation and run
- Install chrome and chromedriver
- Clone the repository from github
- Install python3 >= 3.10
```
https://www.python.org/downloads/
```
- Go to test project
```
cd ~path\to\TestProject
```
- Create and activate Python Virtual ENV
```shell script
python3 -m venv --clear venv

source venv/bin/activate
```
- Install dependencies
```shell script
pip install -r requirements.txt
```
- Run api tests
```shell script
pytest -m user_api_tests
```
- Run UI tests
```shell script
pytest -m user_ui_tests 
```