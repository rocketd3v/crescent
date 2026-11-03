class character:

    def __init__ (self, name, gender):
        self.name = name
        self.gender = gender

        if gender == "male":
            self.sibling = "Mara"
            self.sibling_gender = "Female"
        else:
            self.sibling = "Elliot"
            self.sibling.gender = "Male"

