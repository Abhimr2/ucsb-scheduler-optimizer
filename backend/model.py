from itertools import product

class Scheduler:
    def __init__(self, courses):
        self.courses = courses
    
    def generate_schedules(self):
        allOptions = []
        
        for course in self.courses:
            allOptions.append(course.create_options())
        
        allSchedules = []
        allSchedules = list(product(*allOptions))

        expected = 2 * 2 * 1 * 1
        actual = len(allSchedules)

        validSchedules = []

        for schedule in allSchedules:
            val = self.schedule_is_valid(schedule)

            if val == True:
                validSchedules.append(schedule)
        
        correct = len(validSchedules)

        print("Expected raw schedules:", expected)
        print("Actual raw schedules:", actual)
        print("Valid schedules:", correct)
    
    def schedule_is_valid(self, schedule):
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                if option_conflicts(schedule[i], schedule[j]):
                    return False

        return True

 
class Course:
    def __init__(self, name, code, lectures, sections):
        self.name = name
        self.code = code
        self.lectures = lectures
        self.sections = sections
    
    def create_options(self):
        options = []

        for lecture in self.lectures:
            for section in self.sections:
                options.append([lecture, section])

        return options

    def print_course(self):
        for block in self.meetings:
            
            block.convert_days()

            for day in block.days:
                print(self.name + " (" + self.code + ") has a " + block.type + " from " + str(block.startTime) + " to " + str(block.endTime) + " on " + day)

class Block:
    def __init__(self, days, startTime, endTime, type):
        self.days = days
        self.startTime = startTime
        self.endTime = endTime
        self.type = type
    
    def convert_days(self):
       for i in range(len(self.days)):
        
        if self.days[i] == 'M':
            self.days[i] = 'Monday'
        elif self.days[i] == 'T':
            self.days[i] = 'Tuesday'
        elif self.days[i] == 'W':
            self.days[i] = 'Wednesday'
        elif self.days[i] == 'R':
            self.days[i] = 'Thursday'
        elif self.days[i] == 'F':
            self.days[i] = 'Friday'
    
    def convert_time(self, time):
        time_parts = time.split()
        hour_minute = time_parts[0]
        am_pm = time_parts[1]

        hour, minute = hour_minute.split(":")
        hour = int(hour)
        minute = int(minute)

        if am_pm == "PM" and hour != 12:
            hour += 12

        if am_pm == "AM" and hour == 12:
            hour = 0

        return hour * 60 + minute
    
    def time_to_minutes(self):
        self.startTime = self.convert_time(self.startTime)
        self.endTime = self.convert_time(self.endTime)

def time_conflicts(meeting_a, meeting_b):
    if len(meeting_a.days) == 0 or len(meeting_b.days) == 0:
        return False

    if meeting_a.startTime is None or meeting_a.endTime is None:
        return False

    if meeting_b.startTime is None or meeting_b.endTime is None:
        return False

    shared_day = False

    for day in meeting_a.days:
        if day in meeting_b.days:
            shared_day = True

    if shared_day == False:
        return False

    return meeting_a.startTime < meeting_b.endTime and meeting_b.startTime < meeting_a.endTime

def option_conflicts(option_a, option_b):
    for block_a in option_a:
        for block_b in option_b:
            if time_conflicts(block_a, block_b):
                return True

    return False