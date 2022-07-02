class Lectors(type):
    instances = []

    def __call__(cls, *args, **kwargs):
        instance = super(Lectors, cls).__call__(*args, **kwargs)
        cls.instances.append(instance)

        return instance


class Students(type):
    instances = []

    def __call__(cls, *args, **kwargs):
        instance = super(Students, cls).__call__(*args, **kwargs)
        cls.instances.append(instance)

        return instance


class Student(metaclass=Students):

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lec(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress or course in self.finished_courses \
                and course in lecturer.courses_attached and grade <= 10:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:

            return 'Error'

    def __mid_grades(self):
        sum_grades = 0
        counter = 0
        for grades in self.grades.values():
            for grade in grades:
                counter += 1
                sum_grades += grade
        mid_grade = sum_grades/counter

        return mid_grade

    def __str__(self):
        name = self.name
        surname = self.surname

        return f"Имя: {name}\nФамилия: {surname}\nСредняя оценка за домашние задания: {self.__mid_grades()}\n" \
               f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n" \
               f"Завершенные курсы: {', '.join(self.finished_courses)}"

    def __le__(self, other):
        if not isinstance(other, Student):
            return "Error"

        return self.__mid_grades() <= other.__mid_grades()

    def __lt__(self, other):
        if not isinstance(other, Student):
            return "Error"

        return self.__mid_grades() < other.__mid_grades()


class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor, metaclass=Lectors):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __mid_grades(self):
        sum_grades = 0
        counter = 0
        for grades in self.grades.values():
            for grade in grades:
                counter += 1
                sum_grades += grade
        mid_grade = sum_grades/counter

        return mid_grade

    def __str__(self):
        name = self.name
        surname = self.surname

        return f"Имя: {name}\nФамилия: {surname}\nСредняя оценка за лекции: {self.__mid_grades()}"

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return "Error"

        return self.__mid_grades() <= other.__mid_grades()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return "Error"

        return self.__mid_grades() < other.__mid_grades()


class Reviewer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress\
                and grade <= 10:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:

            return 'Error'

    def __str__(self):
        name = self.name
        surname = self.surname

        return f"Имя: {name}\nФамилия: {surname}"


# Cтудент 1
good_student = Student('Ivan', 'Ivanov', 'mail')
good_student.finished_courses += ['Git']
good_student.courses_in_progress += ['Python']
good_student.grades['Git'] = [10, 10, 10, 10, 10]
good_student.grades['Python'] = [10, 10]

# Cтудент 2
bad_student = Student('Petr', 'Petrov', 'mail')
bad_student.finished_courses += ['Git']
bad_student.courses_in_progress += ['Python']
bad_student.grades['Git'] = [5, 6, 7, 5, 2]
bad_student.grades['Python'] = [10, 3]

# Преподаватель
reviewer = Reviewer('Reviewer', 'Boss')
reviewer.courses_attached += ['Python']

# Оценка первому студенту
reviewer.rate_hw(good_student, 'Python', 8)

# Оценка второму студенту
reviewer.rate_hw(bad_student, 'Python', 6)

# Лектор 1
lector_one = Lecturer('Semen', 'Semenwov')
lector_one.courses_attached += ['Git', 'Python']

# Лектор 2
lector_two = Lecturer('Evgeny', 'Kuznetsov')
lector_two.courses_attached += ['Git', 'Python']

# Первый студент выставил оценку лектору 1
good_student.rate_lec(lector_one, 'Git', 9)
good_student.rate_lec(lector_one, 'Python', 1)

# Второй студент выставил оценку лектору 2
bad_student.rate_lec(lector_two, 'Git', 3)
bad_student.rate_lec(lector_two, 'Python', 9)

# все участнки программы
print(good_student, bad_student, reviewer, lector_two, lector_one, sep='\n \n')

# Сравниваем оценки студентов
print(good_student > bad_student)
print(good_student <= bad_student)

# Сравниваем оценки лекторов
print(lector_two < lector_one)
print(lector_two >= lector_one)


def mid_grades_students(students, course):
    """    подсчет средней оценки за курс у всех студентов    """
    counter = 0
    len_grades = 0
    for student in students:
        counter += sum(student.__dict__['grades'][course])
        len_grades += len(student.__dict__['grades'][course])

    return f"Средняя оценка за курс {course} у всех студентов: {counter / len_grades}"


def mid_grades_lecturers(lecturers, course):
    """    подсчет средней оценки за курс у всех лекторов    """
    counter = 0
    len_grades = 0
    for lecturer in lecturers:
        counter += sum(lecturer.__dict__['grades'][course])
        len_grades += len(lecturer.__dict__['grades'][course])

    return f"Средняя оценка за курс {course} у всех лекторов: {counter / len_grades}"


print(mid_grades_students(Students.instances, 'Git'))
print(mid_grades_lecturers(Lectors.instances, 'Python'))