@echo off
python -m pipenv install
python -m pipenv run python sftp_actions_threaded.py
pause