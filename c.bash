rm FalseRTS 
rm FalseRTS.cpp
git pull
g++ -o FalseRTS FalseRTS.cpp -pthread -std=c++11
./FalseRTS
