## Guardian AI Live Website: https://guardian-ai.herokuapp.com


We have temporarily migrated to Heroku due to a technical issue and will be back on the Google Cloud Soon
https://guardianai-1.df.r.appspot.com/
## Please follow the steps given below to setup the project locally, visit the link given above to view the live version.
### Development

- Clone the repository to your local.
```bash
https://github.com/rajveerbeerda/Guardian-AI.git
```

- Install virtualEnv so you can isolate Python environments.
```bash
sudo pip3 install virtualenv
```

- Navigate to your project directory and create virtualenv with python 3.
```bash
cd Guardian-AI && python3 -m venv env
```

- Activate virtualenv.
```bash
# Activate
source env/bin/activate

# Exit venv with the following command
deactivate
```

- Install requirements for the application.
```bash
pip3 install -r requirements.txt
```

- Run the application.
```bash
python3 main.py
```
