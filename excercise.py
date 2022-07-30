from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

#リモートから得られた画像の物体検出プログラム
subscription_key = "7c8f254564be46faab3cc118e74765b5"   #本来はあまりコードの中で書かない方が良い
endpoint = "https://udemy20220728.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"  #適当な画像のURL

'''
Tag an Image - remote
This example returns a tag (key word) for each thing in the image.
'''
print("===== Tag an image - remote =====")
# Call API with remote image
tags_result_remote = computervision_client.tag_image(remote_image_url )

# Print results with confidence score
print("Tags in the remote image: ")
if (len(tags_result_remote.tags) == 0):
    print("No tags detected.")
else:
    for tag in tags_result_remote.tags:
        print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))

#上のコードによって、画像を分析することができる

##画像カテゴリの取得
print("===== Analyze an image - remote =====")
# Select the visual feature(s) you want.
remote_image_features = ["categories"]

# Call API with URL and features
results_remote = computervision_client.analyze_image(remote_image_url , remote_image_features)

# Print results with confidence score
print("Categories from remote image: ")
if (len(results_remote.categories) == 0):
    print("No categories detected.")
else:
    for category in results_remote.categories:
        print("'{}' with confidence {:.2f}%".format(category.name, category.score * 100))
print()

##画像タグの取得
print("===== Tag an image - remote =====")
tags_result_remote = computervision_client.tag_image(remote_image_url)

#タグには、検出した物体のタグ名が、confidenceには自信度が格納されている
print("Tags in the remote image: ")
if (len(tags_result_remote.tags) == 0):
    print("No tags detected.")
else:
    for tag in tags_result_remote.tags:
        print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))

        
##物体を検出する(戻り値はjson形式)
# Detect objects
# Print detected objects results with bounding boxes
print("===== Detect objects - remote =====")
# Get URL image with defferent objects
remote_image_url_objects = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/objects.jpg"
detect_objects_results_remote = computervision_client.detect_objects(remote_image_url_objects)

#object内には、矩形情報が格納されている。検出した物体がどの位置にどの大きさの長方形内(矩形内)にあるかをjson形式で教えてくれる
print("Detecting objects in remote image:")
if len(results_remote.objects) == 0:
    print("No objects detected.")
else:
    for object in detect_objects_results_remote.objects:
        print("object at location {}, {}, {}, {}".format( \
        object.rectangle.x, object.rectangle.x + object.rectangle.w, \
        object.rectangle.y, object.rectangle.y + object.rectangle.h))

        