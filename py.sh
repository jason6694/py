#!bin/bash
tmux new -s 000000
cd /home/booooob456/000000
python3 LH.py
tmux detach
tmux new -s py3bot1
cd /home/booooob456/py3bot1
python3 bot.py
tmux detach
tmux new -s py3bot5
cd /home/booooob456/py3bot5
python3 bot.py
tmux detach