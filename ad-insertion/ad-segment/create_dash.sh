#!/usr/bin/env bash

set -e

# Usage create-dash.sh SOURCE_FILE
[[ ! "${1}" ]] && echo "Usage: create-dash.sh file minres " && exit 1

# comment/add lines here to control which renditions would be created
renditions=(
# resolution  bitrate  audio-rate
#  "426x240    400k     64k"
  "3840x2160  14000k   192k"
  "2560x1440  10000k   192k"
  "1920x1080  5000k    192k"
  "1280x720   2800k    128k"
  "842x480    1400k    128k"
  "640x360    800k     96k"
)

z_renditions=(
# resolution  bitrate  audio-rate
#  "426x240    400k     64k"
  "640x360    800k     96k"
  "842x480    1400k    128k"
  "1280x720   2800k    128k"
  "1920x1080  5000k    192k"
  "2560x1440  10000k   192k"
  "3840x2160  14000k   192k"
)

segment_target_duration=5000000 # try to create a new segment every X seconds
max_bitrate_ratio=1.07          # maximum accepted bitrate fluctuations
rate_monitor_buffer_ratio=1.5   # maximum buffer size between bitrate conformance checks

#########################################################################

source="segment/archive/${1}"
target="segment/dash/${source##*/}" # leave only last component of path
mkdir -p ${target}

min_height="$(echo ${2} |grep -oE '^[[:digit:]]+')"

if [ -z ${2} ];then
    min_height=360
fi

echo $target
default_threshold=4
count=0

key_frames_interval="$(echo `ffprobe ${source} 2>&1 | grep -oE '[[:digit:]]+(.[[:digit:]]+)? fps' | grep -oE '[[:digit:]]+(.[[:digit:]]+)?'`*2 | bc || echo '')"
key_frames_interval=${key_frames_interval:-50}
key_frames_interval=$(echo `printf "%.1f\n" $(bc -l <<<"$key_frames_interval/10")`*10 | bc) # round
key_frames_interval=${key_frames_interval%.*} # truncate to integer

frame_resolution="$(ffprobe -v error -select_streams v:0 -show_entries stream=height,width -of csv=s=x:p=0 ${source})"
frame_width="$(echo ${frame_resolution} | grep -oE '^[[:digit:]]+')"
frame_height="$(echo ${frame_resolution} | grep -oE '[[:digit:]]+$')"

# static parameters that are similar for all renditions
static_params=" -c:a aac -ar 48000 -c:v libx264 -profile:v main -sc_threshold 0 -strict -2"
static_params+=" -g ${key_frames_interval} -keyint_min ${key_frames_interval}"
static_dash=" -use_timeline 1 -use_template 1  -min_seg_duration ${segment_target_duration}"
#static_dash+=" -adaptation_sets \"id=0,streams=v id=1,streams=a\""

# misc params
misc_params="-hide_banner -y"

cmd_map=""
cmd=""
for rendition in "${renditions[@]}"; do
  # drop extraneous spaces
  rendition="${rendition/[[:space:]]+/ }"

  # rendition fields
  resolution="$(echo ${rendition} | cut -d ' ' -f 1)"
  bitrate="$(echo ${rendition} | cut -d ' ' -f 2)"
  audiorate="$(echo ${rendition} | cut -d ' ' -f 3)"

  # calculated fields
  width="$(echo ${resolution} | grep -oE '^[[:digit:]]+')"
  height="$(echo ${resolution} | grep -oE '[[:digit:]]+$')"
  maxrate="$(echo "`echo ${bitrate} | grep -oE '[[:digit:]]+'`*${max_bitrate_ratio}" | bc)"
  bufsize="$(echo "`echo ${bitrate} | grep -oE '[[:digit:]]+'`*${rate_monitor_buffer_ratio}" | bc)"
  bandwidth="$(echo ${bitrate} | grep -oE '[[:digit:]]+')000"
  name="${height}p"

  if [ ${frame_height} -lt ${height} ] || [ ${height} -lt ${min_height} ]; then
    continue
  fi

  cmd+=" -map 0:v -b:v:${count} ${bitrate} -s:v:${count} ${width}x${height} -maxrate:${count} ${maxrate%.*}k -bufsize:${count} ${bufsize%.*}k "
  cmd+=" -map 0:a -b:a:${count} ${audiorate} -strict -2"
  #cmd+=" -f dash -init_seg_name ${name}-init-\$RepresentationID\$.m4s -media_seg_name ${name}-\$RepresentationID\$-\$Number%05d\$.m4s ${target}/${name}.mpd"

  let count+=1
  if [ ${default_threshold} -lt ${count} ]; then
    break
  fi

done

cmd_param=${cmd_map}
cmd_param+=${static_params}
cmd_param+=${cmd}
cmd_param+=${static_dash}
cmd_param+=" -f dash ${target}/index.mpd"

# start conversion
echo -e "Executing command:\nffmpeg ${misc_params} -i ${source} ${cmd_param}"
ffmpeg ${misc_params} -i ${source} ${cmd_param}

echo "Done - encoded dash is at ${target}/"
