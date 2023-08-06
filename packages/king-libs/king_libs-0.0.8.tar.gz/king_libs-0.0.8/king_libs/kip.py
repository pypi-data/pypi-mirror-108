import os
from random import randint,choice
import shutil

class Kip:

    def __init__(self,data_path,svp_path,f_name,split_rate):

        self.split_name = ['train','test']
        self.data_path = data_path
        self.classes = os.listdir(data_path)
        self.svp_path = svp_path
        self.f_name = f_name
        self.lenght = None
        self.data = None
        self.train_set = None
        self.test_set = None
        self.split_rate = split_rate





    def check_len_projects(self):

        classes = os.listdir(self.data_path)
        try:
            ind = classes.index(self.f_name)
            del classes[ind]
        except :
            pass
        number_of_img = {}
        for cls in classes:
            target_images = os.path.join(self.data_path,cls)
            lenght = len( list(os.listdir(target_images)))
            number_of_img[cls] = lenght


        self.lenght = lenght
        return lenght,number_of_img

    def split(self) :
        train_set = []
        test_set = []
        for cls in self.classes:
            images_path = os.path.join(self.data_path,cls)
            images = os.listdir(images_path)

            per = self.split_rate
            data_size = len(images)
            train_size = round(data_size*(per))
            test_size = data_size-train_size
            cls_img = []
            for num in images[:train_size]:
                img = os.path.join(images_path,num)
                cls_img.append(img)
            train_set.append(cls_img)



            cls_img = []
            for num in images[train_size:]:
                img = os.path.join(images_path,num)
                cls_img.append(img)
            test_set.append(cls_img)



        self.train_set = train_set
        self.test_set = test_set

        return train_set,test_set









    def copy_files(self):


        train = self.train_set
        test = self.test_set
        project = os.path.join(self.svp_path,self.f_name)

        if os.path.exists(project):
            pass
        else:
            os.mkdir(project)

        for ind,cls in enumerate(self.classes):
            if cls == self.f_name:
                pass
            else:
                cls_path = os.path.join(project,'train')
                try:
                    os.mkdir(cls_path)
                except :
                    pass
                classes = os.path.join(cls_path,cls)
                try:
                    os.mkdir(classes)

                except :
                    pass
                for img in train[ind]:

                    name = img.split("\\")[-1]
                    dest = os.path.join(classes,name)
                    src = img
                    dst = dest
                    shutil.copyfile(src,dst)

        for ind,cls in enumerate(self.classes):
            if cls == self.f_name:
                pass
            else:
                cls_path = os.path.join(project,'test')
                try:
                    os.mkdir(cls_path)
                except :
                    pass
                classes = os.path.join(cls_path,cls)
                try:
                    os.mkdir(classes)

                except :
                    pass
                for img in test[ind]:

                    name = img.split("\\")[-1]
                    dest = os.path.join(classes,name)
                    src = img
                    dst = dest
                    shutil.copyfile(src,dst)















