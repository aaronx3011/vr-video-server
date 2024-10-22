#!/bin/bash
 
if [ -z "$(which inotifywait)" ]; then
    echo "inotifywait not installed."
    echo "In most distros, it is available in the inotify-tools package."
    exit 1
fi

counter=0;
 
function execute() {
    counter=$((counter+1))
    echo "Detected change n. $counter" |
    aws s3 sync ./videos/ s3://vrinsitu-aaron-bucket/transmision/ --exclude "*" --include "*.ts"; 
    aws s3 sync ./videos/ s3://vrinsitu-aaron-bucket/transmision/ --exclude "*" --include "*.m3u8"
    eval "$@"
}


inotifywait --recursive --monitor --format "%e %w%f" \
--event move ./ \
--include '.*\.m3u8$' \
| while read changed; do
    echo $changed
    execute "$@"
done
