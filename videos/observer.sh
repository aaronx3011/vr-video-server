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
    aws s3 sync . s3://vrinsitu-aaron-bucket/
    eval "$@"
}
 
inotifywait --recursive --monitor --format "%e %w%f" \
--event modify,move,create,delete ./ \
--include '.*\.ts$' \
| while read changed; do
    echo $changed
    execute "$@"
done
