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


class TeacherCsvSecond(TeacherCsv):

    def __init__(self, full_name, experience: int):
        super().__init__(full_name)
        self.experience = experience

    def save_to_csv(self):
        teacher_header = ['Full_name', 'Exp(years)']
        with open('TeacherSecond.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(teacher_header)
            teacher_data = self.full_name, self.experience
            writer.writerow(teacher_data)
            return writer


t1 = Teacher('Mark Paterson', 6)
t2 = Teacher('Katya Hawever', 8)
TeacherCsvSecond.save_to_csv(TeacherCsvSecond(t2.full_name, t2.experience))


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


class SecondStudent(Student):

    def __init__(self, name, mark: int, left_to_study: int):
        super().__init__(name, mark)
        self.left_study = left_to_study

    def get_mark(self):
        return self.name, self.mark, self.left_study


class SecondStudentCongratulations(StudentCongratulations):

    def __init__(self, name, mark: int, left_to_study: int):
        super().__init__(name, mark)
        self.left_study = left_to_study

    def congratulations(self):
        if self.mark == 100 and self.left_study != 0:
            return f'Congratulations {self.name}, you are the best!!! Left to study {self.left_study} years.'

        elif self.left_study == 0:
            return f'Congratulations on graduation, {self.name}, your mark is {self.mark}'

        else:
            return f'Dont cry, just continue {self.name}. Left to study {self.left_study} years.'


s1 = SecondStudent('Mark', 90, 5)
s2 = SecondStudent('Elon', 100, 0)
s3 = SecondStudent('Artur', 78, 3)
s4 = SecondStudent('Katya', 83, 0)
print(SecondStudentCongratulations.congratulations(SecondStudentCongratulations(s4.name, s4.mark, s4.left_study)))


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


class AverageBothStudentsGroup(BothStudentsGroup):

    def average_students_group(self):
        return f'Average students rounding down {round((self.students1 + self.students2) / 2)}'


g1 = Group('10 B', 30)
g2 = Group('6 A', 18)
g3 = Group('8 E', 27)

print(AverageBothStudentsGroup.average_students_group(AverageBothStudentsGroup(g1.students, g3.students)))
