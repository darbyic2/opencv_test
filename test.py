import cv2
from time import time


##################################################
# Standard camera resolutions
##################################################
# cam_x, cam_y = 640, 480          # VGA or SD or 480p
# cam_x, cam_y = 800, 600          # SVGA
cam_x, cam_y = 1280, 720         # HD or 720p
# cam_x, cam_y = 1920, 1080        # FHD (Full HD) or 1080p
# cam_x, cam_y = 2560, 1440        # QHD (Quad HD) or 2K video
# cam_x, cam_y = 3840, 2160        # UHD (Ultra HD) or 4K video
# cam_x, cam_y = 7680, 4320        # 8K video


def packedFccToString(fcc):
    return f'{chr(fcc & 0xff)}{chr((fcc >> 8) & 0xff)}{chr((fcc >> 16) & 0xff)}{chr((fcc >> 24) & 0xff)}'

cap = cv2.VideoCapture(0, cv2.CAP_V4L)

if cap.isOpened():
    print("Initial capture settings...")
    print("codec:", packedFccToString(int(cap.get(cv2.CAP_PROP_FOURCC))))
    print("Resolution:", int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), "x", int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("Brightness:", int(cap.get(cv2.CAP_PROP_BRIGHTNESS)))
    print("Contrast:", int(cap.get(cv2.CAP_PROP_CONTRAST)))

    # Change capture codec, resolution, brilliance, and contrast
    cap.set(cv2.CAP_PROP_FOURCC, int(cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_x)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_y)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 150)
    cap.set(cv2.CAP_PROP_CONTRAST, 100)

    print("\nAfter changes...")
    print("codec:", packedFccToString(int(cap.get(cv2.CAP_PROP_FOURCC))))
    print("Resolution:", int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), "x", int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("Brightness:", int(cap.get(cv2.CAP_PROP_BRIGHTNESS)))
    print("Contrast:", int(cap.get(cv2.CAP_PROP_CONTRAST)))

else:
    print("Webcam capture failed to start")

prevTime = time()

while cap.isOpened() and True:
    success, img = cap.read()

    if success:
        # Process captured image

        # Stamp frame rate on to finished image
        curTime = time()
        fps = int(1 / (curTime - prevTime))
        prevTime = curTime
        cv2.putText(img, f'FPS: {fps}', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        # Display webcam image
        cv2.imshow("Webcam", img)

    else:
        print("Web feed ended.")
        break

    # User can press 'q' at any time to end the stream
    if cv2.waitKey(1) & 0xff == ord('q'):
        print("User quit.")
        break

# Clean up any used resources
cap.release()
cv2.destroyAllWindows()
