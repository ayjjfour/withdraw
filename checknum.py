# -*- encoding=utf-8 -*-

import os

from svmutil import *
from PIL import Image


def get_bin_table():
    threshold = 150  
    table = []  
    for i in range(256):  
        if i < threshold:  
            table.append(0)  
        else:
            table.append(1)
            
    return table

def sum_9_region(img, x, y):
    """
    9�����,�Ե�ǰ��Ϊ���ĵ����ֿ�,�ڵ����
    :param x:
    :param y:
    :return:
    """
    # todo �ж�ͼƬ�ĳ��������
    cur_pixel = img.getpixel((x, y))  # ��ǰ���ص��ֵ
    width, height = img.size
    psum = 0

    if cur_pixel == 1:  # �����ǰ��Ϊ��ɫ����,��ͳ������ֵ
        return 0

    if y == 0:  # ��һ��
        if x == 0:  # ���϶���,4����
            # ���ĵ��Ա�3����
            psum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - psum
        elif x == width - 1:  # ���϶���
            psum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - psum
        else:  # ���ϷǶ���,6����
            psum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - psum
    elif y == height - 1:  # ������һ��
        if x == 0:  # ���¶���
            # ���ĵ��Ա�3����
            psum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - psum
        elif x == width - 1:  # ���¶���
            psum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - psum
        else:  # ���·Ƕ���,6����
            psum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - psum
    else:  # y���ڱ߽�
        if x == 0:  # ��߷Ƕ���
            psum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - psum
        elif x == width - 1:  # �ұ߷Ƕ���
            # print('%s,%s' % (x, y))
            psum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - psum
        else:  # �߱�9����������
            psum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - psum    

def remove_single_point(img):
    width, height = img.size
    
    #print "width = ", width, "Height = ", height
    
    for h in range(height):
        for w in range(width):
            total = sum_9_region(img, w, h)
            if total < 2 :
                img.putpixel((w, h), 1)

def fliter_points(img):
    #cur_pixel = img.getpixel((x, y))  # ��ǰ���ص��ֵ
    width, height = img.size
    
    #print "width = ", width, "Height = ", height
    
    for h in range(height):
        for w in range(width):
            if (h < 5 or h > 16) or (w < 6 or w > 40):
                img.putpixel((w, h), 1)
                continue
            
            if (w == 14 or w == 23 or w == 32):
                img.putpixel((w, h), 1)
                continue
            
    #ȥ�������ĵ�
    remove_single_point(img)            
    
def get_crop_imgs(img):
    """
    ����ͼƬ���ص�,�����и�,���Ҫ���ݾ������֤�������й���. # ��ԭ��ͼ
    :param img:
    :return:
    """
    child_img_list = []
    for i in range(4):
        x = 6 + i * (8 + 1)  # ��ԭ��ͼ
        y = 5
        child_img = img.crop((x, y, x + 8, y + 12))
        child_img_list.append(child_img)

    return child_img_list
   
def open_img_01(img_path):
    image = Image.open(img_path)
    imgry = image.convert('L')  # ת��Ϊ�Ҷ�ͼ
    table = get_bin_table()
    out = imgry.point(table, '1')
    return out
   
def Change_gray(count):
    #print "start gray"
    j = 0
    for i in range(count):
        img_path = 'd:\pic\createImg_%d.jpg' %i
        save_path = 'd:\pic\createImg2_%d.jpg' %i
        out = open_img_01(img_path)
        
        fliter_points(out)
        list_img = get_crop_imgs(out)
        for im in range(len(list_img)):
            list_img[im].save('d:\\pic\\test\\%d.jpg' %j)
            j += 1
            
        out.save(save_path)
        #print "out =", out
    
    #print "Finish gray"
        
    return
    
def Create_test_feature(count):
    list_test = build_feature('d:\\pic\\test')
    f = open('d:\\pic\\last_test_pix_xy_new.txt', 'w+')
    
    line_size = len(list_test)
    for line in range(line_size):
        str_line = "1"
        row_size = len(list_test[line])
        for row in range(row_size):
            str_line = str_line + " %(row)d:%(val)d" %{'row':row + 1, 'val':list_test[line][row]}
        print >>f, str_line
    
def get_feature(img):
    """
                ��ȡָ��ͼƬ������ֵ,
    1. ����ÿ�ŵ����ص�,�߶�Ϊ12,����12��ά��,Ȼ��Ϊ8��,�ܹ�20��ά��
    :param img_path:
    :return:һ��ά��Ϊ10���߶ȣ����б�
    """
    width, height = img.size

    pixel_cnt_list = []
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:  # ��ɫ��
                pix_cnt_x += 1

        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:  # ��ɫ��
                pix_cnt_y += 1

        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list

def build_feature(rootdir):
    pixel_cnt_list = []
    for parent, _, filenames in os.walk(rootdir):    #�����������ֱ𷵻�1.��Ŀ¼ 2.�����ļ������֣�����·���� 3.�����ļ�����
        for filename in filenames:
            fullname =  os.path.join(parent,filename) #����ļ�·����Ϣ
            #print "the full name of the file is:" + fullname
            image = open_img_01(fullname)
            list_f = get_feature(image)
            pixel_cnt_list.append(list_f)
            
    return pixel_cnt_list

    
def create_feature_txt():
    """
    for i in range(256):
        im = Image.open('d:\pic\createImg2_%d.jpg' %i)
        imgry = im.convert('L')
        text = pytesseract.image_to_string(imgry)
        print "text(%d) =" %i, text
    return
    """
    
    f = open('d:\\pic\\train_pix_feature_xy.txt', 'w+')
    for i in range(10):
        rootdir = 'd:\pic\\nums\%d' %i
        pixel_cnt_list = build_feature(rootdir)
        line_size = len(pixel_cnt_list)
        for line in range(line_size):
            str_line = "%d" % i
            row_size = len(pixel_cnt_list[line])
            for row in range(row_size):
                str_line = str_line + " %(row)d:%(val)d" %{'row':row + 1, 'val':pixel_cnt_list[line][row]}
            print >>f, str_line
            

def train_svm_model():
    """
    ѵ��������model�ļ�
    :return:
    """
    y, x = svm_read_problem('d:\\pic\\train_pix_feature_xy.txt')
    model = svm_train(y, x)
    svm_save_model('d:\\pic\\aa.model', model)

def svm_model_test(model):
    """
    ʹ�ò��Լ�����ģ��
    :return:
    """
    yt, xt = svm_read_problem('d:\\pic\\last_test_pix_xy_new.txt')
    #p_lab, p_acc, p_val = svm_predict(yt, xt, model)#p_label��Ϊʶ��Ľ��
    p_lab, _, _ = svm_predict(yt, xt, model)
    verifycode = "%(n1)d%(n2)d%(n3)d%(n4)d" % {"n1":p_lab[0], "n2":p_lab[1], "n3":p_lab[2], "n4":p_lab[3]}

    return verifycode
    """
    cnt = 0
    for item in p_lab:
        print('item=%d' % item)
        cnt += 1
        if cnt % 8 == 0:
            print('')
    """

def check_num():
    model = svm_load_model('d:\\pic\\aa.model')
    Change_gray(1)
    Create_test_feature(1)
    verifycode = svm_model_test(model)
    
    return verifycode
