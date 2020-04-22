# Home-Buying

### Development

- Install virtualEnv so you can isolate Python environments.
```bash
sudo pip3 install virtualenv
```

- Go to your Project directory and create virtualenv with python 3.
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
