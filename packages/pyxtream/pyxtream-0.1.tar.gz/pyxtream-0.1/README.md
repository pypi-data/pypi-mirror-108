# pyxtream
Loads xtream IPTV

# Build PIP Module
python3 setup.py bdist_wheel

# Install
python3 -m pip install dist/pyxtream-0.1-py3-none-any.whl

# Record TS Video
ffmpeg -y -i "(iptv url)" -c:v copy -c:a copy  -map 0:v -map 0:a -t 00:00:30 "myrecording.ts" >"mylog.log" 2>&1
