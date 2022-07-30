from tkinter import W
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json

with open('secret.json') as f:
    secret = json.load(f)
    
subscription_key = secret['KEY']
endpoint = secret['ENDPOINT']    

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

#関数の用意
def get_tags(filepath):
    local_image = open(filepath, "rb")

    ##タグ(名前と自信度(%))を取得する
    #ローカルイメージに対してAPIを呼び出す
    tags_result_local = computervision_client.tag_image_in_stream(local_image)

    #タグをリスト形式で獲得する
    tags = tags_result_local.tags

    #空のリスト(名前のみ)を作成
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
                         
    return tags_name

##物体の場所がどこにあるのかを検出する
def detect_objects(filepath):
    local_image = open(filepath, "rb")

    detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image)
    objects =  detect_objects_results_local.objects
    
    return objects
    

import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

st.title('物体検出アプリ')
uploaded_file = st.file_uploader('Choose an image...', type = ['jpg','pmg'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)   
    
    #img画像を作業フォルダに入れて、アップロードしたファイルの名前を取得する
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_objects(img_path)
   
    
    ##描画(図に書き込む)
    draw = ImageDraw.Draw(img)
    #座標情報を元に、矩形を座標と一致させる
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h        
        caption = object.object_property
        
        font = ImageFont.truetype(font = './Helvetica Bold.ttf',size = 50)
        text_w,text_h = draw.textsize(caption, font = font)
        
        #矩形の出力(物体用と名前用)
        draw.rectangle([(x,y),(x+w, y+h)],fill = None,outline = 'green',width = 5)
        draw.rectangle([(x,y),(x+text_w, y+text_h)],fill = None, outline = 'green', width = 5)
        draw.text((x,y), caption, fill = 'White', font = font)
    st.image(img)
    
    tags_name = get_tags(img_path)
    tags_name = ', '.join(tags_name)
    st.markdown('**認識されたコンテンツタグ**')
    st.markdown(f'> {tags_name}')


