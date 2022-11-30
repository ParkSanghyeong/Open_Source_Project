import os
import sys
import image_processing
import ocr

#===================================================================================================
#   argument :  target img path
if len(sys.argv) != 2:
    sys.exit("Invalid Argument Input")

target_img_path = sys.argv[1]

if (os.path.exists(target_img_path) == False) :
    sys.exit("File not found")
#===================================================================================================
#Object Detection Part
print("[Object Detection Start]")

#target_img = "test.jpg"
command_detect = "python ./yolov5/detect.py --weights ./weight/best.pt --source " + target_img_path
command_detect_para = " --save-crop --project result --name img_table --exist-ok --nosave"

try :
    #Empty the result folder
    filePath = "./result/img_table/crops/table"
    if os.path.exists(filePath) :
        for file in os.scandir(filePath) :
            os.remove(file.path)

    #Start Detection
    #Note: Calculation takes a long time
    os.system(command_detect + command_detect_para)
except :
    sys.exit("Error : Object Detection")

print("[Object Detection End]")
#===================================================================================================
#image processing
#print("[Image Processing Start]")
try :
    croped_img_path = "./result/img_table/crops/table/"
    croped_img = os.listdir(croped_img_path)[0]

    source_path = croped_img_path + croped_img
    save_path = "./result/binary/" + "binary.jpg"

    #Empty the result folder
    filePath = "./result/binary/"
    if os.path.exists(filePath) :
        for file in os.scandir(filePath) :
            os.remove(file.path)

    #save binary threshold image
    image_processing.get_binary_thres(source_path, save_path)
except :
    sys.exit("Error : Image Processing")

#print("[Image Processing End]")
#===================================================================================================
#OCR Part
#print("[OCR Start]")
try :
    res = ocr.get_ocr()
except :
    sys.exit("Error : OCR")
#print("[OCR End]")

info = ocr.sorting(res)
ocr.recalculate(info)
#===================================================================================================