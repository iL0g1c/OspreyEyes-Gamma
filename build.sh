rm -r -f build
mkdir build
cd build
mkdir OEG
cd OEG
cp ../../src/.env .
cp ../../src/callsigns.py .
cp ../../src/api.py .
cp ../../src/chat.py .
cp ../../src/OEG.py .
cp ../../requirements.txt .
cp ../../src/playerCount.py .