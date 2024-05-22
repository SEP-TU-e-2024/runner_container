mkdir runenv

cp -r submission/** /runenv
cp -r validator/** /runenv

cd runenv

python main.py
ls -la /