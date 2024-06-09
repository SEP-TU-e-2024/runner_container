mkdir runenv

cd runenv
pipenv shell

pipenv install -r submission/requirements.txt
pipenv install -r validator/requirements.txt

cp -r /submission/** ./
cp -r /validator/** ./

python main.py