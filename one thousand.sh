#!/bin/bash
for i in {1..100}
do
	xterm -hold -e python client.py &
done