import time
import picamera
import exifread

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 1 
    # Wait for the automatic gain control to settle
    #camera.iso = 100
    #for i in range(20):
        #print "shuter %d" % camera.exposure_speed
        #time.sleep(0.1)

    
    time.sleep(2)
    camera.iso = 100
    for i in range(20):
        print "shuter %d" % camera.exposure_speed
        time.sleep(0.1)
    camera.time = 2
    camera.capture("test.jpg")
    f = open("test.jpg", "rb")
    tags = exifread.process_file(f, details=False)
    print tags["EXIF ExposureTime"]
    print tags["EXIF ISOSpeedRatings"]
    #iso = int("%s" % tags["EXIF ISOSpeedRatings"])
    #print iso
    #camera.shutter_speed = camera.exposure_speed
    #camera.exposure_mode = 'off'
    #g = camera.awb_gains
    #camera.awb_mode = 'off'
    #camera.awb_gains = g
    #print camera.shutter_speed
    # Finally, take several photos with the fixed settings
    #camera.capture_sequence(['image%02d.jpg' % i for i in range(10)])
