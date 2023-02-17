rm -r blocks/Alice
rm -r blocks/Bob

python3.10 bob.py &
sleep 2
python3.10 alice.py &
