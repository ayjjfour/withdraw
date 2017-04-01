# -*- encoding=utf-8 -*-

import os

from svmutil import *
from PIL import Image

check_path = os.getcwd()

""" 创建学习model的方法，目前不需要
def build_feature(rootdir):
    pixel_cnt_list = []
    for parent, _, filenames in os.walk(rootdir):
        for filename in filenames:
            fullname =  os.path.join(parent,filename)
            #print "the full name of the file is:" + fullname
            image = open_img_01(fullname)
            list_f = get_feature(image)
            pixel_cnt_list.append(list_f)
            
    return pixel_cnt_list

    
def create_feature_txt():
    f = open(check_path + '/svm/train_pix_feature_xy.txt', 'w+')
    for i in range(10):
        rootdir = check_path + '/pic/nums/%d' % i
        pixel_cnt_list = build_feature(rootdir)
        line_size = len(pixel_cnt_list)
        for line in range(line_size):
            str_line = "%d" % i
            row_size = len(pixel_cnt_list[line])
            for row in range(row_size):
                str_line = str_line + " %(row)d:%(val)d" %{'row':row + 1, 'val':pixel_cnt_list[line][row]}
            print >>f, str_line

def train_svm_model():
    y, x = svm_read_problem(check_path + '/svm/train_pix_feature_xy.txt')
    model = svm_train(y, x)
    svm_save_model(check_path + '/svm/svm.model', model)
"""
###############################################封装成类###############################################

class CheckNum(object):
    def __init__(self, mfile = None):
        if mfile == None:
            self.model = None
        else:
            self.model = svm_load_model(mfile)
            
        self.featurefile = check_path + '/pic/last_test_pix_xy_new.txt'
    
    def check_num(self, imgfile):
        pixel_cnt_list = self._change_gray(imgfile)
        self._create_num_feature(pixel_cnt_list, self.featurefile)
        verifycode = self._get_result(self.featurefile) #svm_model_test(model)
        
        return verifycode
        
    # 将彩图变成黑白图，然后分割数字并取得每个数字的特征值
    def _change_gray(self, imgfile):
        #print "start gray"
        out = self._open_img_01(imgfile)
            
        self._fliter_points(out)
        list_img = self._get_crop_imgs(out)
        pixel_cnt_list = []
        for im in range(len(list_img)):
            list_f = self._get_feature(list_img[im])
            pixel_cnt_list.append(list_f)
            
        return pixel_cnt_list

    def _open_img_01(self, img_path):
        image = Image.open(img_path)
        imgry = image.convert('L')
        table = self._get_bin_table()
        out = imgry.point(table, '1')
        return out
    
    def _fliter_points(self, img):
        width, height = img.size
       
        for h in range(height):
            for w in range(width):
                if (h < 5 or h > 16) or (w < 6 or w > 40):
                    img.putpixel((w, h), 1)
                    continue
                
                if (w == 14 or w == 23 or w == 32):
                    img.putpixel((w, h), 1)
                    continue

        self._remove_single_point(img)
    
    def _remove_single_point(self, img):
        width, height = img.size
        
        for h in range(height):
            for w in range(width):
                total = self._sum_9_region(img, w, h)
                if total < 2 :
                    img.putpixel((w, h), 1)
    
    def _sum_9_region(self, img, x, y):
        cur_pixel = img.getpixel((x, y))
        width, height = img.size
        psum = 0
    
        if cur_pixel == 1:
            return 0
    
        if y == 0:
            if x == 0:
                psum = cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
                return 4 - psum
            elif x == width - 1:
                psum = cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1))
    
                return 4 - psum
            else:
                psum = img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
                return 6 - psum
        elif y == height - 1:
            if x == 0:
                psum = cur_pixel \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x, y - 1))
                return 4 - psum
            elif x == width - 1:
                psum = cur_pixel \
                      + img.getpixel((x, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y - 1))
    
                return 4 - psum
            else:
                psum = cur_pixel \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x, y - 1)) \
                      + img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x + 1, y - 1))
                return 6 - psum
        else:
            if x == 0:
                psum = img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
    
                return 6 - psum
            elif x == width - 1:
                # print('%s,%s' % (x, y))
                psum = img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1))
    
                return 6 - psum
            else:
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
    
    # 图片二值化，0表示黑，1表示白
    def _get_bin_table(self):
        threshold = 150  
        table = []  
        for i in range(256):  
            if i < threshold:  
                table.append(0)  
            else:
                table.append(1)
                
        return table
    
    # 提取子图片，把每个数字单独分割出来
    def _get_crop_imgs(self, img):
        child_img_list = []
        for i in range(4):
            x = 6 + i * (8 + 1)
            y = 5
            child_img = img.crop((x, y, x + 8, y + 12))
            child_img_list.append(child_img)

        return child_img_list
    
    def _get_feature(self, img):
        width, height = img.size
    
        pixel_cnt_list = []
        for y in range(height):
            pix_cnt_x = 0
            for x in range(width):
                if img.getpixel((x, y)) == 0:
                    pix_cnt_x += 1
    
            pixel_cnt_list.append(pix_cnt_x)
    
        for x in range(width):
            pix_cnt_y = 0
            for y in range(height):
                if img.getpixel((x, y)) == 0:
                    pix_cnt_y += 1
    
            pixel_cnt_list.append(pix_cnt_y)
    
        return pixel_cnt_list
    
    def _create_num_feature(self, list_test, featurefile):
        f = open(featurefile, 'w+')
    
        line_size = len(list_test)
        for line in range(line_size):
            str_line = "1"
            row_size = len(list_test[line])
            for row in range(row_size):
                str_line = str_line + " %(row)d:%(val)d" %{'row':row + 1, 'val':list_test[line][row]}
            print >>f, str_line
        
        f.close()
            
            
    def _get_result(self, featurefile):
        yt, xt = svm_read_problem(featurefile)
        #p_lab, p_acc, p_val = svm_predict(yt, xt, model)
        p_lab, _, _ = svm_predict(yt, xt, self.model)
        verifycode = "%(n1)d%(n2)d%(n3)d%(n4)d" % {"n1":p_lab[0], "n2":p_lab[1], "n3":p_lab[2], "n4":p_lab[3]}
    
        return verifycode