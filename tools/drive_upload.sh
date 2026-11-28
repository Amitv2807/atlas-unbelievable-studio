#!/bin/bash
# Upload a big video to the owner's Google Drive (resumable Drive API upload, 64 MB chunks, resumes after errors).
#   drive_upload.sh FILE "Name in Drive"   -> prints the new file id; link: https://drive.google.com/file/d/<id>/view
# Needs a network secret for www.googleapis.com (Authorization: Bearer <token>) from developers.google.com/oauthplayground,
# scope https://www.googleapis.com/auth/drive.file; tokens last ~1 hour. Body PUTs must carry Content-Type: video/mp4 (the proxy refuses form bodies).
F="$1"; NAME="$2"; S=$(mktemp -d); SZ=$(stat -c%s "$F"); CH=$((64*1024*1024))
URI=$(curl -s -D - -o /dev/null -X POST "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&fields=id,name,size" \
  -H "Content-Type: application/json; charset=UTF-8" -H "X-Upload-Content-Type: video/mp4" -H "X-Upload-Content-Length: $SZ" \
  --data "{\"name\":\"$NAME\",\"mimeType\":\"video/mp4\"}" | tr -d '\r' | awk -F': ' 'tolower($1)=="location"{print $2}')
[ -n "$URI" ] || { echo "no upload session"; exit 1; }
off=0; tries=0
while [ $off -lt $SZ ]; do
  end=$((off+CH-1)); [ $end -ge $SZ ] && end=$((SZ-1)); len=$((end-off+1))
  code=$(tail -c +$((off+1)) "$F" | head -c $len | curl -s -D $S/h.txt -o $S/resp.txt -w "%{http_code}" -X PUT -H "Content-Type: video/mp4" -H "Content-Length: $len" -H "Content-Range: bytes $off-$end/$SZ" --data-binary @- "$URI")
  if [ "$code" = "200" ] || [ "$code" = "201" ]; then echo "DONE"; cat $S/resp.txt; exit 0; fi
  if [ "$code" = "308" ]; then r=$(tr -d '\r' < $S/h.txt | awk -F': ' 'tolower($1)=="range"{print $2}'); off=$(( ${r##*-} + 1 )); tries=0; echo "$((off*100/SZ))% ($off/$SZ)"; continue; fi
  tries=$((tries+1)); echo "chunk at $off failed: HTTP $code (try $tries)"; [ $tries -gt 5 ] && exit 1; sleep $((tries*3))
  q=$(curl -s -D $S/h.txt -o /dev/null -w "%{http_code}" -X PUT -H "Content-Length: 0" -H "Content-Range: bytes */$SZ" "$URI"); r=$(tr -d '\r' < $S/h.txt | awk -F': ' 'tolower($1)=="range"{print $2}'); [ -n "$r" ] && off=$(( ${r##*-} + 1 ))
done
