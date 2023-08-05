from PIL import Image
import numpy as np
import cv2
import os

labels = {0: 'Face', 1: 'Shirt', 2: 'Trouser', 3: 'Dress', 4: 'Coat', 5: 'Sandal', 6: 'Boot', 7: 'Handgun', 8: 'Shotgun', 9: 'Knife'}
  
class ObjectDetection:
    def __init__(self):

        self.model = None
        self.model_type = None

    def set_model(self, model='tinyyolov4'):

        if not model == 'tinyyolov4':
            raise RuntimeError('Invalid Model Type')
        else:
            self.model_type = model

    
    def load_model(self, input_shape:int = 608):
        
        classes_path = os.path.dirname(os.path.abspath(__file__))+'/weights/classes.names'
        base_path = os.path.dirname(os.path.abspath(__file__))+'/weights/'

        if self.model_type == 'tinyyolov4':

            from yolov4.tf import YOLOv4 as yolo_main
            self.model = yolo_main(tiny=True)
            self.model.input_size = input_shape
            self.model.classes = classes_path
            self.model.make_model()
            self.model.load_weights(base_path+'yolov4-tiny-final.weights', weights_type = 'yolo')

        else:
            raise RuntimeError('Invalid Model Type')
        
    
    def get_image(self, img:np.ndarray, output_path:str, iou = 0.45, score = 0.1, custom_objects:dict = None,
                debug=True):

        #img = np.array(Image.open(img))[..., ::-1] 
        pred_bboxes = self.model.predict(img, iou_threshold = iou, score_threshold = score)
        
        boxes = []
        if (custom_objects != None):
          for i in range(len(pred_bboxes)):
            check_name = labels[int(pred_bboxes[i][4])]
            check = custom_objects.get(check_name, 'invalid')
            if check == 'invalid':
              continue
            elif check == 'valid':
              boxes.append(list(pred_bboxes[i]))
          boxes = np.array(boxes)
          res = self.model.draw_bboxes(img, boxes)
          if debug:
            cv2.imwrite(output_path, res)

        else:
          res = self.model.draw_bboxes(img, pred_bboxes)
          if debug:
              cv2.imwrite(output_path, res)
        
        return res
    
    
    def get_prediction(self, img:np.ndarray, iou = 0.45, score = 0.1):
        
        pred_bboxes = self.model.predict(img, iou_threshold = iou, score_threshold = score)
        return pred_bboxes