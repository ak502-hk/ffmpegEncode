@echo off
setlocal enabledelayedexpansion

set "input_folder=S:\temp"
set "output_folder=S:\temp\upload"
set "max_size=2000000" REM 2GB in kilobytes

for %%f in ("%input_folder%\*.mp4") do (
  set input_file=%%~ff
  set output_file=%output_folder%\%%~nf-720p.mp4
  
  REM Use FFprobe to extract video duration
  set "duration="
  for /f "tokens=*" %%a in ('ffprobe -v error -show_entries format^=duration^ -of default^=noprint_wrappers^=1:nokey^=1 "%%~f"') do set "duration=%%a"

  REM Get the audio bit rate
  set "audio_bit_rate="
  for /f "tokens=*" %%a in ('ffprobe -v error -select_streams a:0 -show_entries stream^=bit_rate -of default^=noprint_wrappers^=1:nokey^=1 "%%~f"') do set "audio_bit_rate=%%a"
  
  REM Calculate the bit rate base on duration and audio bit rate
  set /a "video_bit_rate=((max_size * 8) - (audio_bit_rate/1000 * duration)) / duration"
  
  REM encode the video by new bit rate and using nvidia display card
  ffmpeg -hwaccel cuda -i "!input_file!" -c:v h264_nvenc -b:v !video_bit_rate!k -vf scale=1280:720 -c:a aac -b:a 128k "!output_file!"  

)
