# Guardian AI Live Website: https://guardian-ai-1.df.r.appspot.com/
## Please follow the steps given below to setup the project locally, visit the link given above to view the live version.
### Development

- Clone the repository to your local.
```bash
git clone https://github.com/rajveerbeerda/Home-Buying.git
```

- Install virtualEnv so you can isolate Python environments.
```bash
sudo pip3 install virtualenv
```

- Navigate to your project directory and create virtualenv with python 3.
```bash
cd ~/Home-Buying && virtualenv venv -p python3
```

- Activate virtualenv.
```bash
# Activate
source venv/bin/activate

# Exit venv with the following command
deactivate
```

- Install requirements for the application.
```bash
pip3 install requirements.txt
```

- Run the application.
```bash
python3 app.py
```
