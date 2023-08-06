import base64
import cv2

def img_base64(img):    #图片转换base64函数
    with open(img,"rb") as f:#转为二进制格式
        base64_data = base64.b64encode(f.read())#使用base64进行加密
        return str(base64_data,'utf-8')

def img_frame(img_url,data):
    frame=cv2.imread(img_url)   #打开图片准备画框
    if data:
        if data['error_code']==0:
            for i in data['result']['face_list']:  #使用遍历把所有的人脸信息
                location=i['location']  #获取每张人脸的坐标信息
                print(location)   #输出人脸坐标 left location是左上角坐标：其中 width代表宽度 , height代表高度 , left、top分别代表人脸左上角坐标
                cv2.rectangle(frame,(int(location['left']), int(location['top'])), (int(location['width']+location['left']), int(location['height']+location['top'])), (0,255,0), 2)
                #在图上画出脸的位置
    cv2.imshow('face',frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()