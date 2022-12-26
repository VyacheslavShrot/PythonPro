import csv


class Teacher:

    def __init__(self, full_name, experience: int):
        self.full_name = full_name
        self.experience = experience

    def show(self):
        return self.full_name, self.experience


class TeacherCsv:

    def __init__(self, full_name):
        self.full_name = full_name

    def save_to_csv(self):
        teacher_header = ['Full_name']
        with open('Teacher.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(teacher_header)
            teacher_data = [self.full_name]
            writer.writerow(teacher_data)
            return writer


t1 = Teacher('Mark Paterson', 6)
t2 = Teacher('Katya Hawever', 8)
TeacherCsv.save_to_csv(TeacherCsv(t1.full_name))


class Student:

    def __init__(self, name, mark: int):
        self.name = name
        self.mark = mark

    def get_mark(self):
        return self.mark, self.name


class StudentCongratulations:

    def __init__(self, name, mark: int):
        self.name = name
        self.mark = mark

    def congratulations(self):
        if self.mark == 100:
            return f'Congratulations {self.name}, you are the best!!!'

        else:
            return f'Dont cry, just continue {self.name}'


s1 = Student('Mark', 90)
s2 = Student('Elon', 100)
s3 = Student('Artur', 78)
s4 = Student('Katya', 83)

print(StudentCongratulations.congratulations(StudentCongratulations(s2.name, s2.mark)))


class Group:

    def __init__(self, group_name, students: int):
        self.group_name = group_name
        self.students = students

    def group(self):
        return self.group_name, self.students


class BothStudentsGroup:

    def __init__(self, students1: int, students2: int):
        self.students1 = students1
        self.students2 = students2

    def both_students_group(self):
        return self.students1 + self.students2


g1 = Group('10 B', 30)
g2 = Group('6 A', 18)
g3 = Group('8 E', 27)

print(BothStudentsGroup.both_students_group(BothStudentsGroup(g1.students, g3.students)))
