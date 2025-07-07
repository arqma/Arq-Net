mkdir arq$1
cd arq$1
ln -s ../arqnet arqnet$1
cp ../arqnet.ini .
nano arqnet.ini
cd ..
echo "killall -9 arqnet$1" >> ../stop.sh
