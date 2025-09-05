gst-launch-1.0 rtspsrc location=rtsp://192.168.88.114:554/stream protocols=tcp ! rtph265depay ! h265parse ! nvh265dec ! queue ! tee name=t rtmpsrc location=rtmp://192.168.88.116:1950/live/origin1 ! flvdemux ! tee name= t0 rtmpsrc location=rtmp://192.168.88.116:1950/live/origin1 ! tee name= t1 rtmpsrc location=rtmp://192.168.88.116:1950/live/origin1 ! tee name= t2 rtmpsrc location=rtmp://192.168.88.116:1950/live/origin1 ! queue ! fakesink t0. ! queue ! fakesink t1. ! queue ! fakesink t2. ! fakesink t. ! queue ! videoconvert ! autovideosink













gst-launch-1.0 rtspsrc location=rtsp://192.168.88.102:554/stream onvif-mode=true ! rtph265depay ! h265parse ! nvh265dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! tee name=notstitchedstream1 alsasrc device=hw:1 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! tee name=at rtmpsrc location=rtmp://192.168.88.211:1950/live/origin1  ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin2  ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin3  ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin4  ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/templatecam1campovenbol.pts crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45 ! video/x-raw\(memory:GLMemory\),format=RGBA,width=7680,height=4320 ! tee name=t t. ! queue ! nvh265enc preset = 1 ! h265parse ! queue ! mux0. at.  ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8kSTITCHED1%05d.ts playlist-location=videos/high/8kSTITCHED1.m3u8 t. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! mux1. at. ! queue ! mpegtsmux name=mux1 ! hlssink target-duration=15 location=videos/high/4kSTITCHED1%05d.ts playlist-location=videos/high/4kSTITCHED1.m3u8 t. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! mux2. at. ! queue ! mpegtsmux name=mux2 ! hlssink target-duration=15 location=videos/low/2kSTITCHED1%05d.ts playlist-location=videos/low/2kSTITCHED1.m3u8 t. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! mux3. at. ! queue ! mpegtsmux name=mux3 ! hlssink target-duration=15 location=videos/low/1kSTITCHED1%05d.ts playlist-location=videos/low/1kSTITCHED1.m3u8 notstitchedstream1.  ! queue ! nvh265enc preset = 1 ! h265parse ! queue ! notstitchedmux10. at.  ! queue ! mpegtsmux name=notstitchedmux10 ! hlssink target-duration=15 location=videos/high/8kNOTSTITCHED1%05d.ts playlist-location=videos/high/8kNOTSTITCHED1.m3u8 notstitchedstream1. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! notstitchedmux11. at.  ! queue ! mpegtsmux name=notstitchedmux11 ! hlssink target-duration=15 location=videos/high/4kNOTSTITCHED1%05d.ts playlist-location=videos/high/4kNOTSTITCHED1.m3u8 notstitchedstream1. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! notstitchedmux12. at.  ! queue ! mpegtsmux name=notstitchedmux12 ! hlssink target-duration=15 location=videos/low/2kNOTSTITCHED1%05d.ts playlist-location=videos/low/2kNOTSTITCHED1.m3u8 notstitchedstream1. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! notstitchedmux13. at.  ! queue ! mpegtsmux name=notstitchedmux13 ! hlssink target-duration=15 location=videos/low/1kNOTSTITCHED1%05d.ts playlist-location=videos/low/1kNOTSTITCHED1.m3u8

#
#
#
#
#
#
#
#
# gst-launch-1.0 -e  \
#     rtspsrc location=rtsp://192.168.88.102:554/stream ! \
#         rtph265depay ! h265parse ! queue ! nvh265dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     tee name=solocamera alsasrc device=hw:1 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! \
#     tee name=at rtmpsrc location=rtmp://192.168.88.211:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin4 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin3 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin2 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. gldmdstitcher name=mix client=vrinsitu1 template=/home/vrinsitu/Documents/vr-video-server/stitch-templates/CircularTitan.pts crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45 ! video/x-raw\(memory:GLMemory\),format=RGBA,width=7680,height=4320 ! tee name=t t. ! \
#         queue ! nvh265enc preset = 1 ! h265parse ! queue ! \
#             mux0. at. ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8kTESTING25MB15S265%05d.ts playlist-location=videos/high/8kTESTING25MB15S265.m3u8 t. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! \
#             hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265%05d.ts playlist-location=videos/high/4kTESTING25MB15S265.m3u8 t. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! \
#             hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265%05d.ts playlist-location=videos/low/2kTESTING25MB15S265.m3u8 t. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! \
#             hlssink target-duration=15 location=videos/low/1kTESTING25MB15S265%05d.ts playlist-location=videos/low/1kTESTING25MB15S265.m3u8 t. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh264enc preset = 1 ! h264parse ! \
#             hlssink target-duration=15 location=videos/low/10kTESTING25MB15S265%05d.ts playlist-location=videos/low/10kTESTING25MB15S265.m3u8 solocamera. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! \
#             hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265CAM2%05d.ts playlist-location=videos/high/4kTESTING25MB15S265CAM2.m3u8 solocamera. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! \
#             hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265CAM2%05d.ts playlist-location=videos/low/2kTESTING25MB15S265CAM2.m3u8 solocamera. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh264enc preset = 1 ! h264parse ! \
#             hlssink target-duration=15 location=videos/low/10kTESTING25MB15S265CAM2%05d.ts playlist-location=videos/low/10kTESTING25MB15S265CAM2.m3u8
# 







gst-launch-1.0 rtspsrc location=rtsp://192.168.88.102:554/stream onvif-mode=true ! rtph265depay ! h265parse ! nvh265dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! tee name=notstitchedstream1  alsasrc device=hw:2 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! tee name=at rtmpsrc location=rtmp://192.168.88.211:1950/live/origin1 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin2 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin3 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin4 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/template.pts crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45 ! video/x-raw\(memory:GLMemory\),format=RGBA,width=7680,height=4320 ! tee name=t t. ! queue ! fakesink notstitchedstream1. ! queue ! glimagesink





# gst-launch-1.0 rtspsrc location=rtsp://192.168.88.102:554/stream ! rtph265depay ! h265parse ! nvh265dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! tee name=notstitchedstream1  alsasrc device=hw:1 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! tee name=at rtmpsrc location=rtmp://192.168.88.211:1950/live/origin1 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin2 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin3 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin4 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/template.pts crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45 ! video/x-raw\(memory:GLMemory\),format=RGBA,width=7680,height=4320 ! tee name=t t. ! queue ! nvh265enc preset = 1 ! h265parse ! queue ! mux0. at.  ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8kSTITCHED1%05d.ts playlist-location=videos/high/8kSTITCHED1.m3u8 t. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! mux1. at. ! queue ! mpegtsmux name=mux1 ! hlssink target-duration=15 location=videos/high/4kSTITCHED1%05d.ts playlist-location=videos/high/4kSTITCHED1.m3u8 t. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! mux2. at. ! queue ! mpegtsmux name=mux2 ! hlssink target-duration=15 location=videos/low/2kSTITCHED1%05d.ts playlist-location=videos/low/2kSTITCHED1.m3u8 t. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! mux3. at. ! queue ! mpegtsmux name=mux3 ! hlssink target-duration=15 location=videos/low/1kSTITCHED1%05d.ts playlist-location=videos/low/1kSTITCHED1.m3u8 notstitchedstream1.  ! queue ! nvh265enc preset = 1 ! h265parse ! queue ! notstitchedmux10. at.  ! queue ! mpegtsmux name=notstitchedmux10 ! hlssink target-duration=15 location=videos/high/8kNOTSTITCHED1%05d.ts playlist-location=videos/high/8kNOTSTITCHED1.m3u8 notstitchedstream1. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! notstitchedmux11. at.  ! queue ! mpegtsmux name=notstitchedmux11 ! hlssink target-duration=15 location=videos/high/4kNOTSTITCHED1%05d.ts playlist-location=videos/high/4kNOTSTITCHED1.m3u8 notstitchedstream1. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! notstitchedmux12. at.  ! queue ! mpegtsmux name=notstitchedmux12 ! hlssink target-duration=15 location=videos/low/2kNOTSTITCHED1%05d.ts playlist-location=videos/low/2kNOTSTITCHED1.m3u8 notstitchedstream1. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! notstitchedmux13. at.  ! queue ! mpegtsmux name=notstitchedmux13 ! hlssink target-duration=15 location=videos/low/1kNOTSTITCHED1%05d.ts playlist-location=videos/low/1kNOTSTITCHED1.m3u8





















#
# gst-launch-1.0 alsasrc device=hw:1 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! tee name=at rtmpsrc location=rtmp://192.168.88.211:1950/live/origin1 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin1 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin1 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin1 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! mix. gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/LumixFullFrame.pts crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45 ! video/x-raw\(memory:GLMemory\),format=RGBA,width=7680,height=4320 ! tee name=t t. ! queue ! nvh265enc preset = 1 ! h265parse ! queue ! mux0. at.  ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8kTESTING25MB15S265%05d.ts playlist-location=videos/high/8kTESTING25MB15S265.m3u8 t. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! mux1. at. ! queue ! mpegtsmux name=mux1 ! hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265%05d.ts playlist-location=videos/high/4kTESTING25MB15S265.m3u8 t. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! mux2. at. ! queue ! mpegtsmux name=mux2 ! hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265%05d.ts playlist-location=videos/low/2kTESTING25MB15S265.m3u8 t. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! mux3. at. ! queue ! mpegtsmux name=mux3 ! hlssink target-duration=15 location=videos/low/1kTESTING25MB15S265%05d.ts playlist-location=videos/low/1kTESTING25MB15S265.m3u8













#
# not stitched fino
gst-launch-1.0 rtspsrc location=rtsp://192.168.88.102:554/stream ! rtph265depay ! h265parse ! nvh265dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! tee name=notstitchedt0 ! queue ! nvh265enc preset = 1 ! h265parse ! queue ! mux0. alsasrc device=hw:1 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! tee name=at  ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8kTESTING25MB15S265%05d.ts playlist-location=videos/high/8kTESTING25MB15S265.m3u8 notstitchedt0. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! mux1. at. ! queue ! mpegtsmux name=mux1 ! hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265%05d.ts playlist-location=videos/high/4kTESTING25MB15S265.m3u8 notstitchedt0. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! mux2. at. ! queue ! mpegtsmux name=mux2 ! hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265%05d.ts playlist-location=videos/low/2kTESTING25MB15S265.m3u8 notstitchedt0. ! queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! mux3. at. ! queue ! mpegtsmux name=mux3 ! hlssink target-duration=15 location=videos/low/1kTESTING25MB15S265%05d.ts playlist-location=videos/low/1kTESTING25MB15S265.m3u8









# gst-launch-1.0 -e  \
#     rtspsrc location=rtsp://192.168.88.102:554/stream ! \
#         rtph265depay ! h265parse ! queue ! nvh265dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     tee name=solocamera rtmpsrc location=rtmp://192.168.88.211:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin4 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin3 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.211:1950/live/origin2 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. gldmdstitcher name=mix client=vrinsitu1 template=/home/vrinsitu/Documents/vr-video-server/stitch-templates/CircularTitan.pts crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45 ! video/x-raw\(memory:GLMemory\),format=RGBA,width=7680,height=4320 ! tee name=t t. ! \
#         queue ! nvh265enc preset = 1 ! h265parse ! queue ! \
#             hlssink target-duration=15 location=videos/high/8kTESTING25MB15S265%05d.ts playlist-location=videos/high/8kTESTING25MB15S265.m3u8 t. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! \
#             hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265%05d.ts playlist-location=videos/high/4kTESTING25MB15S265.m3u8 t. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! \
#             hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265%05d.ts playlist-location=videos/low/2kTESTING25MB15S265.m3u8 t. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! \
#             hlssink target-duration=15 location=videos/low/1kTESTING25MB15S265%05d.ts playlist-location=videos/low/1kTESTING25MB15S265.m3u8 t. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh264enc preset = 1 ! h264parse ! \
#             hlssink target-duration=15 location=videos/low/10kTESTING25MB15S265%05d.ts playlist-location=videos/low/10kTESTING25MB15S265.m3u8 solocamera. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! \
#             hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265CAM2%05d.ts playlist-location=videos/high/4kTESTING25MB15S265CAM2.m3u8 solocamera. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! \
#             hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265CAM2%05d.ts playlist-location=videos/low/2kTESTING25MB15S265CAM2.m3u8 solocamera. ! \
#         queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh264enc preset = 1 ! h264parse ! \
#             hlssink target-duration=15 location=videos/low/10kTESTING25MB15S265CAM2%05d.ts playlist-location=videos/low/10kTESTING25MB15S265CAM2.m3u8




# gst-launch-1.0 -e  \
#     rtmpsrc location=rtmp://192.168.88.23:1950/live/origin5 ! \
#     tee name=solocamera rtmpsrc location=rtmp://192.168.88.23:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.23:1950/live/origin4 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.23:1950/live/origin3 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.23:1950/live/origin2 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/template.pts crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45 ! video/x-raw\(memory:GLMemory\),format=RGBA,width=7680,height=4320 ! glimagesink solocamera. ! queue ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! glimagesink
#
#
#
#
#
#
#
# GST_DEBUG=4 gst-launch-1.0 \
#     rtspsrc location=rtsp://192.168.88.72:554/stream ! tee name=test ! queue ! rtph265depay ! queue ! fakesink test. ! fakesink ! \
#     rtspsrc location=rtsp://192.168.88.72:554/stream ! tee name=test ! queue ! rtph265depay ! queue ! fakesink test. ! fakesink
    










# gst-launch-1.0 \
#     rtspsrc location=rtsp://192.168.88.72:554/stream ! queue ! tee name=input1 input1. ! queue ! rtph265depay ! h265parse ! queue ! nvh265dec ! videoconvert ! autovideosink input1. ! \
#     queue ! fakesink










# rtspsrc location=rtsp://192.168.88.72:554/stream ! tee name=input1 input1. ! queue ! rtpmp4gdepay ! aacparse ! avdec_aac ! audioconvert ! autoaudiosink 

# gst-launch-1.0 \
#     rtspsrc location=rtsp://192.168.88.72:554/stream ! tee name=input1 input1. ! \
#         queue ! rtph265depay ! h265parse ! \
#             queue ! nvh265dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#                 queue ! nvh265enc preset = 1 ! h265parse ! queue ! input1. ! \
#         queue ! rtpmp4gdepay ! aacparse ! \
#             queue ! avdec_aac ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! \
#         queue ! mpegtsmux name=mux4 ! hlssink target-duration=15 location=videos/low/10kTESTING25MB15S265%05d.ts playlist-location=videos/low/10kTESTING25MB15S265.m3u8




# rtmpsrc location=rtmp://192.168.88.46:1950/live/origin1 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw(memory:GLMemory) ! glcolorconvert ! video/x-raw(memory:GLMemory),format=RGBA ! tee name=t0rtmpsrc location=rtmp://192.168.88.46:1950/live/origin2 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw(memory:GLMemory) ! glcolorconvert ! video/x-raw(memory:GLMemory),format=RGBA ! tee name=t1rtmpsrc location=rtmp://192.168.88.46:1950/live/origin3 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw(memory:GLMemory) ! glcolorconvert ! video/x-raw(memory:GLMemory),format=RGBA ! tee name=t2rtmpsrc location=rtmp://192.168.88.46:1950/live/origin4 ! flvdemux ! h264parse ! nvh264dec ! video/x-raw(memory:GLMemory) ! glcolorconvert ! video/x-raw(memory:GLMemory),format=RGBA ! tee name=t3


# queue ! nvh265enc preset = 1 ! h265parse ! queue ! mux0. alsasrc device=hw:0 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! tee name=at  ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8kTESTING25MB15S265%05d.ts playlist-location=videos/high/8kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! mux1. at. ! queue ! mpegtsmux name=mux1 ! hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265%05d.ts playlist-location=videos/high/4kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! mux2. at. ! queue ! mpegtsmux name=mux2 ! hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265%05d.ts playlist-location=videos/low/2kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! mux3. at. ! queue ! mpegtsmux name=mux3 ! hlssink target-duration=15 location=videos/low/1kTESTING25MB15S265%05d.ts playlist-location=videos/low/1kTESTING25MB15S265.m3u8queue ! nvh265enc preset = 1 ! h265parse ! queue ! mux0. alsasrc device=hw:0 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! tee name=at  ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8kTESTING25MB15S265%05d.ts playlist-location=videos/high/8kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! mux1. at. ! queue ! mpegtsmux name=mux1 ! hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265%05d.ts playlist-location=videos/high/4kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! mux2. at. ! queue ! mpegtsmux name=mux2 ! hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265%05d.ts playlist-location=videos/low/2kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! mux3. at. ! queue ! mpegtsmux name=mux3 ! hlssink target-duration=15 location=videos/low/1kTESTING25MB15S265%05d.ts playlist-location=videos/low/1kTESTING25MB15S265.m3u8queue ! nvh265enc preset = 1 ! h265parse ! queue ! mux0. alsasrc device=hw:0 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! tee name=at  ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8kTESTING25MB15S265%05d.ts playlist-location=videos/high/8kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! mux1. at. ! queue ! mpegtsmux name=mux1 ! hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265%05d.ts playlist-location=videos/high/4kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! mux2. at. ! queue ! mpegtsmux name=mux2 ! hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265%05d.ts playlist-location=videos/low/2kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! mux3. at. ! queue ! mpegtsmux name=mux3 ! hlssink target-duration=15 location=videos/low/1kTESTING25MB15S265%05d.ts playlist-location=videos/low/1kTESTING25MB15S265.m3u8queue ! nvh265enc preset = 1 ! h265parse ! queue ! mux0. alsasrc device=hw:0 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! tee name=at  ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8kTESTING25MB15S265%05d.ts playlist-location=videos/high/8kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! mux1. at. ! queue ! mpegtsmux name=mux1 ! hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265%05d.ts playlist-location=videos/high/4kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! mux2. at. ! queue ! mpegtsmux name=mux2 ! hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265%05d.ts playlist-location=videos/low/2kTESTING25MB15S265.m3u8 toutput . ! queue ! glcolorscale ! video/x-raw(memory:GLMemory), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! mux3. at. ! queue ! mpegtsmux name=mux3 ! hlssink target-duration=15 location=videos/low/1kTESTING25MB15S265%05d.ts playlist-location=videos/low/1kTESTING25MB15S265.m3u8






# gst-launch-1.0 -e \
#     alsasrc device=hw:0 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! \
#     tee name=at rtmpsrc location=rtmp://192.168.88.46:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     tee name=test rtmpsrc location=rtmp://192.168.88.46:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.46:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.46:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.46:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/template.pts crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45 ! video/x-raw\(memory:GLMemory\),format=RGBA,width=7680,height=4320 ! \
#     tee name=t t. ! queue ! nvh265enc preset = 1 ! h265parse ! queue ! \
#     mux0. at. ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8kTESTING25MB15S265%05d.ts playlist-location=videos/high/8kTESTING25MB15S265.m3u8 t. ! \
#     queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! \
#         mux1. at. ! queue ! mpegtsmux name=mux1 ! hlssink target-duration=15 location=videos/high/4kTESTING25MB15S265%05d.ts playlist-location=videos/high/4kTESTING25MB15S265.m3u8 t. ! \
#     queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! \
#         mux2. at. ! queue ! mpegtsmux name=mux2 ! hlssink target-duration=15 location=videos/low/2kTESTING25MB15S265%05d.ts playlist-location=videos/low/2kTESTING25MB15S265.m3u8 t. ! \
#     queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! \
#         mux3. at. ! queue ! mpegtsmux name=mux3 ! hlssink target-duration=15 location=videos/low/1kTESTING25MB15S265%05d.ts playlist-location=videos/low/1kTESTING25MB15S265.m3u8 test. ! \
#     queue ! glcolorscale ! video/x-raw\(memory:GLMemory\), width=3840, height=2160 ! nvh264enc preset = 1 ! h264parse ! \
#         mux4. at. ! queue ! mpegtsmux name=mux4 ! hlssink target-duration=15 location=videos/low/10kTESTING25MB15S265%05d.ts playlist-location=videos/low/10kTESTING25MB15S265.m3u8















# gst-launch-1.0 -e  \
#     rtmpsrc location=rtmp://192.168.88.16:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:glmemory\) ! glcolorconvert ! video/x-raw\(memory:glmemory\),format=rgba ! \
#     mix. rtmpsrc location=rtmp://192.168.88.16:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:glmemory\) ! glcolorconvert ! video/x-raw\(memory:glmemory\),format=rgba ! \
#     mix. rtmpsrc location=rtmp://192.168.88.16:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:glmemory\) ! glcolorconvert ! video/x-raw\(memory:glmemory\),format=rgba ! \
#     mix. rtmpsrc location=rtmp://192.168.88.16:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:glmemory\) ! glcolorconvert ! video/x-raw\(memory:glmemory\),format=rgba ! \
#     mix. gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/template.pts crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45 ! video/x-raw\(memory:glmemory\),format=rgba,width=7680,height=4320 ! \
#     tee name=t t. ! queue ! nvh265enc preset = 1 ! h265parse ! queue ! \
#     mux0. alsasrc device=hw:0 ! queue ! audioconvert ! audioresample ! audio/x-raw,rate=48000,channels=2,width=16 ! avenc_aac ! aacparse ! \
#     tee name=at at. ! queue ! mpegtsmux name=mux0 ! hlssink target-duration=15 location=videos/high/8ktesting25mb15s265%05d.ts playlist-location=videos/high/8ktesting25mb15s265.m3u8 t. ! \
#     queue ! glcolorscale ! video/x-raw\(memory:glmemory\), width=3840, height=2160 ! nvh265enc preset = 1 ! h265parse ! \
#         mux1. at. ! queue ! mpegtsmux name=mux1 ! hlssink target-duration=15 location=videos/high/4ktesting25mb15s265%05d.ts playlist-location=videos/high/4ktesting25mb15s265.m3u8 t. ! \
#     queue ! glcolorscale ! video/x-raw\(memory:glmemory\), width=2560, height=1440 ! nvh264enc preset = 1 ! h264parse ! \
#         mux2. at. ! queue ! mpegtsmux name=mux2 ! hlssink target-duration=15 location=videos/low/2ktesting25mb15s265%05d.ts playlist-location=videos/low/2ktesting25mb15s265.m3u8 t. ! \
#     queue ! glcolorscale ! video/x-raw\(memory:glmemory\), width=2600, height=900 ! nvh264enc preset = 1 ! h264parse ! \
#         mux3. at. ! queue ! mpegtsmux name=mux3 ! hlssink target-duration=15 location=videos/low/1ktesting25mb15s265%05d.ts playlist-location=videos/low/1ktesting25mb15s265.m3u8






# gst-launch-1.0 -e  \
#     rtmpsrc location=rtmp://192.168.88.23:1950/live/origin5 ! \
#     tee name=solocamera rtmpsrc location=rtmp://192.168.88.23:1950/live/origin1 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.23:1950/live/origin4 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.23:1950/live/origin3 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. rtmpsrc location=rtmp://192.168.88.23:1950/live/origin2 ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! \
#     mix. gldmdstitcher name=mix client=vrinsitu1 template=stitch-templates/template.pts crop-left=-90 crop-right=90 crop-bottom=-45 crop-top=45 ! video/x-raw\(memory:GLMemory\),format=RGBA,width=7680,height=4320 ! glimagesink solocamera. ! queue ! \
#         flvdemux ! h264parse ! nvh264dec ! video/x-raw\(memory:GLMemory\) ! glcolorconvert ! video/x-raw\(memory:GLMemory\),format=RGBA ! glimagesink
