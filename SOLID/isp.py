import random


class RandomLimitGroup:

    @staticmethod
    def group_limit():
        students_limit = random.randint(20, 30)
        return f"limit {students_limit} students"


class RandomLimitTeacher:

    @staticmethod
    def teacher_limit():
        group_limit = random.randint(3, 7)
        return f"has {group_limit} groups on this year"


class RandomLimitStudents:

    @staticmethod
    def students_limit():
        lessons_limit = random.randint(5, 8)
        return f"students will receive {lessons_limit} lessons"


class Group(RandomLimitGroup):

    def __init__(self, group_name):
        self.group_name = group_name

    def group_limit(self):
        return f"In group {self.group_name} {RandomLimitGroup.group_limit()}"


print(Group.group_limit(Group('10-B')))


class Teacher(RandomLimitTeacher):

    def __init__(self, teacher_name):
        self.full_name = teacher_name

    def teacher_limit(self):
        return f"{self.full_name} {RandomLimitTeacher.teacher_limit()}"


print(Teacher.teacher_limit(Teacher('Artur Patherson')))


class Students(RandomLimitStudents):

    def __init__(self, students: int):
        self.students = students

    def students_limit(self):
        return f"On Monday {self.students} {RandomLimitStudents.students_limit()}"


print(Students.students_limit(Students(30)))
