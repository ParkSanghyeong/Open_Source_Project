import os
import image_processing

#===================================================================================================
#Object Detection Part
print("Object Detection Start")

target_img = "test.jpg"

command_detect = "python ./yolov5/detect.py --weights ./weight/best.pt --source ./imgs/"
command_detect_para = " --save-crop --project result --name img_table --exist-ok --nosave"

#Empty the result folder
filePath = "./result/img_table/crops/table"
if os.path.exists(filePath) :
    for file in os.scandir(filePath) :
        os.remove(file.path)

#Start Detection
#Note: Calculation takes a long time
os.system(command_detect + target_img + command_detect_para)

#===================================================================================================
#image processing
print("Image Processing Start")

source_path = "./result/img_table/crops/table/" + target_img
save_path = "./result/binary/" + "binary.jpg"

#Empty the result folder
filePath = "./result/binary/"
if os.path.exists(filePath) :
    for file in os.scandir(filePath) :
        os.remove(file.path)

#save binary threshold image
image_processing.get_binary_thres(source_path, save_path)

#===================================================================================================
#OCR Part