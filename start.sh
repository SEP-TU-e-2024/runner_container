mkdir runenv

pip install -r submission/requirements.txt
pip install -r validator/requirements.txt

cp -r submission/** /runenv
cp -r validator/** /runenv

cd runenv

python main.py