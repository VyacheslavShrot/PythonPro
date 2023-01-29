

class Group:

    def __init__(self, group_name, main_students: int):
        self.attr = {'name': group_name, 'students': main_students}

    def group(self, max_students=35):

        if self.attr['students'] <= max_students:
            return f"Group {self.attr['name']} is confirm"

        else:
            return f'Limit students is {max_students}'


class Teacher(Group):

    def group(self, max_students=25):

        if self.attr['students'] <= max_students:
            return f"Teacher get group {self.attr['name']}"

        else:
            return f'Limit students is {max_students}'


class Student(Group):

    def group(self, max_students=17):

        if self.attr['students'] <= max_students:
            return f"Group {self.attr['name']} wait for teacher"

        else:
            return f'Limit students is {max_students}'


g1 = Group('8-A', 28)
g2 = Teacher(g1.attr['name'], g1.attr['students'])
g3 = Student('11-D', 16)
students = (g1, g2, g3)


for student in students:
    if student.attr['students'] <= 27:
        print(student.attr['name'], student.attr['students'])

print(g1.group())
print(g2.group(max_students=28))
print(g3.group())
