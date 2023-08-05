def sayhello():
    print("Hello")

class Person:
    def __init__(self, fname="Andy", lname="King", age=24, gender="M", interests=[]):
        self.fname = fname
        self.lname = lname
        self.age = age
        self.gender = gender
        self.interests = interests
    
    def introduce_self(self):
        print("Hi, I'm {} {}. I'm {} years old.".format(self.fname, self.lname, self.age))
        return

    def add_interest(self, interest):
        if not interest in self.interests:
            self.interests.append(interest)
        return

    def add_interests(self, interests):
        for interest in interests:
            if not interest in self.interests:
                self.interests.append(interest)
        return