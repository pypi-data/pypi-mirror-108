import pandas as pd
import os
import io 
import cv2
import numpy as np
from keras.models import load_model
from .detector.face_detector import MTCNNFaceDetector
#from detector import face_detector
import tensorflow as tf
from models.elg_keras import KerasELG

class Diagnose():
    def __init__(self):
        pass

        
    def Image_croping(self , image , detect_model_path):
        """ return left eye and right eye image cropped"""
       ## loading wieghts
        fd = MTCNNFaceDetector(sess=tf.compat.v1.keras.backend.get_session(), model_path= detect_model_path) # loading face detection model
        face, lms = fd.detect_face(image) # detect the number of faces 
        if len(face) == 1 : 
            left_eye_im, right_eye_im = fd.cropImage(image,lms)
            return left_eye_im , right_eye_im , face
        if len(face) > 1 :
            return 'Multiple faces detected' , 'Multiple faces detected'  , face
        return 'No face detected' ,  'No face detected' , face


    def Eyes_diagnosis(self, left_eye_im , right_eye_im , diagnosis_model_path):

        """ return description and probability of disease for each eye"""
        diagnosis_model_path = os.path.join(os.path.dirname(__file__), diagnosis_model_path)
        model = load_model(diagnosis_model_path) # load disease detection model 
        ############################# left eye #############################
        left_eye_im = cv2.resize(left_eye_im, (100, 100))  
        left_eye_im = left_eye_im.reshape(1 ,100 , 100 , -1)

        left_eye_im_diagnosis = model.predict(left_eye_im)

        if left_eye_im_diagnosis > 0.56:
            left_eye_im_desc =  ' Left Eye : Cataract detected'
        else :
            left_eye_im_desc = 'Left Eye : No Cataract detected'


        ############################# right eye #############################
        right_eye_im = cv2.resize(right_eye_im, (100, 100))
        right_eye_im = right_eye_im.reshape(1 ,100 , 100 , -1)
        right_eye_im_diagnosis  = model.predict(right_eye_im)

        if right_eye_im_diagnosis > 0.56:
            right_eye_im_desc =  'Right Eye : Cataract detected'
        else :
            right_eye_im_desc = 'Right Eye : No Cataract detected'

        return left_eye_im_desc ,left_eye_im_diagnosis[0], right_eye_im_desc , right_eye_im_diagnosis[0]

    def Diagnose_patient(self , image , detect_model_path , diagnosis_model_path):
        
        """ return croped eye image, diagnosis descripition and probability for both eyes ( 6 output items) """
    
        left_eye_im , right_eye_im , face = self.Image_croping(image , detect_model_path) # crop eyes & ensure image is good for diagnosis

        if len(face) != 1 :
            return left_eye_im , left_eye_im, left_eye_im , left_eye_im , left_eye_im , left_eye_im  

        left_eye_im_desc ,left_eye_im_diagnosis, right_eye_im_desc , right_eye_im_diagnosis = self.Eyes_diagnosis(left_eye_im , right_eye_im , diagnosis_model_path) # diagnosis 

        return left_eye_im , left_eye_im_desc , left_eye_im_diagnosis , right_eye_im , right_eye_im_desc , right_eye_im_diagnosis

    def eyeChecker(self, lms):
        last = 0
        xs = []
        for i, lm in enumerate(np.squeeze(lms)):
            last = i - 1 if i != 0 else 0
            #print(last)
            x, y = int(lm[0]*3), int(lm[1]*3)
            xs.append(x)
            if i>0 and i<5:
                if x - xs[last] < 0:
                    return False
            elif i>=5 and i<8:
                if x - xs[last] > 0:
                    return False
            elif i>=8 and i<13:
                if x - xs[last] < 0:
                    return False
            elif i>=13 and i<16:
                if x - xs[last] > 0:
                    return False

        return True

    def Diagnose_patient_2(self, img, diagnosis_model_path):
        model = KerasELG()
        model.net.load_weights("./elg_weights/elg_keras.h5")
        #img = cv2.imread(img_path)[..., ::-1]
        inp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        inp = cv2.equalizeHist(inp)
        inp = cv2.resize(inp, (180,108))[np.newaxis, ..., np.newaxis]
        pred = model.net.predict(inp/255 * 2 - 1)
        lms = model._calculate_landmarks(pred)
        if self.eyeChecker(lms):
            diagnosis_model_path = os.path.join(os.path.dirname(__file__), diagnosis_model_path)
            model2 = load_model(diagnosis_model_path) # load disease detection model
            #return 'This is an Eye'
            eye_im = cv2.resize(img, (100, 100))  
            eye_im = eye_im.reshape(1 ,100 , 100 , -1)
            eye_im_diagnosis = model2.predict(eye_im)
            if eye_im_diagnosis > 0.56:
                eye_im_desc =  'Cataract detected'
            else :
                eye_im_desc = 'No Cataract detected'
        else: 
            return 'This is not an Eye', 'This is not an Eye'

        return eye_im_diagnosis[0],eye_im_desc

        
