import os

train_img_dir = "SHWD/images/train"
val_img_dir = "SHWD/images/val"
test_img_dir = "SHWD/images/test"
train_label_dir = "SHWD/labels/train"
val_label_dir = "SHWD/labels/val"
test_label_dir = "SHWD/labels/test"

os.makedirs(train_img_dir)
os.makedirs(val_img_dir)
os.makedirs(test_img_dir)
os.makedirs(train_label_dir)
os.makedirs(val_label_dir)
os.makedirs(test_label_dir)
