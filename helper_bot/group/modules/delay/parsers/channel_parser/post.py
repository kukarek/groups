

class Post():

    def __init__(self) -> None:
        self.image = None
        
    def set_id(self, id):
        self.id = id

    def set_time(self, datetime):

        self.datetime = datetime

    def set_text(self, text):
        self.text = text

    def set_image(self, image):
        self.image = image
