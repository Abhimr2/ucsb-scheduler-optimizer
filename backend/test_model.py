from model import Course, Block, Scheduler, time_conflicts, option_conflicts
from itertools import product

# -------------------------
# TEST CODE
# -------------------------

# Course 1: Math
math_lecture_1 = Block(["M", "W"], "9:00 AM", "9:50 AM", "Lecture")
math_lecture_2 = Block(["T", "R"], "9:00 AM", "10:15 AM", "Lecture")
math_section_1 = Block(["F"], "9:00 AM", "9:50 AM", "Section")

# Course 2: Computer Science
cs_lecture_1 = Block(["M", "W"], "10:00 AM", "10:50 AM", "Lecture")
cs_lecture_2 = Block(["T", "R"], "9:30 AM", "10:45 AM", "Lecture")  # conflicts with math_lecture_2
cs_section_1 = Block(["F"], "10:00 AM", "10:50 AM", "Section")

# Course 3: Music
music_lecture_1 = Block(["M", "W"], "1:00 PM", "1:50 PM", "Lecture")
music_section_1 = Block(["F"], "1:00 PM", "1:50 PM", "Section")

# Course 4: Writing
writing_lecture_1 = Block(["T", "R"], "2:00 PM", "3:15 PM", "Lecture")
writing_section_1 = Block(["W"], "2:00 PM", "2:50 PM", "Section")

# Create courses
math = Course("Math", "MATH", [math_lecture_1, math_lecture_2], [math_section_1])
cs = Course("Computer Science", "CS", [cs_lecture_1, cs_lecture_2], [cs_section_1])
music = Course("Music", "MUS", [music_lecture_1], [music_section_1])
writing = Course("Writing", "WRIT", [writing_lecture_1], [writing_section_1])

# Convert all times
for course in [math, cs, music, writing]:
    for block in course.lectures:
        block.time_to_minutes()

    for block in course.sections:
        block.time_to_minutes()

# Create scheduler
scheduler = Scheduler([math, cs, music, writing])

# Run generate_schedules()
print("Testing generate_schedules:")
scheduler.generate_schedules()
print()

# Manually create schedules to test schedule_is_valid
allOptions = []

for course in scheduler.courses:
    allOptions.append(course.create_options())

allSchedules = list(product(*allOptions))

print("Testing schedule_is_valid:")

for i in range(len(allSchedules)):
    schedule = allSchedules[i]
    is_valid = scheduler.schedule_is_valid(schedule)

    print("Schedule", i + 1, "valid:", is_valid)

print()
print("Expected:")
print("Raw schedules should be 4")
print("Valid schedules should be 3")
print("Schedule 4 should be invalid")
print()
print("Done testing.")