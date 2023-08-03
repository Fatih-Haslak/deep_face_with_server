from deepface import DeepFace

class ClassDeepFace():
    def __init__(self):
        pass

    def run(self,image1,image2):
        result  = DeepFace.verify(image1, image2)
        return result
    

