class HomophoneNotFound(BaseException):

     def __init__(self):
        self.message = f"Word doesn't have Homophone"