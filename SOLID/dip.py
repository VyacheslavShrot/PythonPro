from abc import ABC, abstractmethod


class Lesson(ABC):

    @abstractmethod
    def start_lesson(self):
        pass

    @abstractmethod
    def finish_lesson(self):
        pass


class Group(Lesson):

    def start_lesson(self):
        print('Gather a group to start the lesson\n')

    def finish_lesson(self):
        print("The lesson is over, prepare everyone for the next lesson\n")


class Teacher(Lesson):

    def start_lesson(self):
        print('Need to go teach students\n')

    def finish_lesson(self):
        print('Prepare for the next lesson\n')


class Students(Lesson):

    def start_lesson(self):
        print('Start the lesson, need to go to class\n')

    def finish_lesson(self):
        print('Lesson is over, break is start)\n')


class SchoolLesson:

    def __init__(self, g: Lesson):
        self.lesson = g
        self.on = False

    def school_lesson(self):

        if self.on:
            self.lesson.start_lesson()

        else:
            self.lesson.finish_lesson()
            self.on = True


g1 = Group()
t1 = Teacher()
s1 = Students()


lessons_switch_gr = SchoolLesson(g1)
lessons_switch_gr.school_lesson()
lessons_switch_gr.school_lesson()


lessons_switch_th = SchoolLesson(t1)
lessons_switch_th.school_lesson()
lessons_switch_th.school_lesson()


lessons_switch_st = SchoolLesson(s1)
lessons_switch_st.school_lesson()
lessons_switch_st.school_lesson()
