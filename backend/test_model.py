import io
import unittest
from contextlib import redirect_stdout

from model import (
    Block,
    Course,
    Scheduler,
    time_conflicts,
    option_conflicts,
)


class TestBlock(unittest.TestCase):
    def test_convert_time(self):
        block = Block([], None, None, "Test")

        cases = {
            "9:05 AM": 545,
            "12:00 AM": 0,
            "12:00 PM": 720,
            "1:00 PM": 780,
        }

        for time, expected in cases.items():
            with self.subTest(time=time):
                self.assertEqual(block.convert_time(time), expected)

    def test_time_to_minutes(self):
        block = Block(["M"], "1:00 PM", "1:50 PM", "Lecture")
        block.time_to_minutes()

        self.assertEqual(block.startTime, 780)
        self.assertEqual(block.endTime, 830)

    def test_convert_days(self):
        block = Block(["M", "T", "W", "R", "F"], 540, 590, "Lecture")
        block.convert_days()

        self.assertEqual(
            block.days,
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        )


class TestConflicts(unittest.TestCase):
    def test_time_conflicts(self):
        cases = [
            (
                Block(["M"], 540, 600, "Lecture"),
                Block(["M"], 570, 630, "Lecture"),
                True,
            ),
            (
                Block(["M"], 540, 600, "Lecture"),
                Block(["M"], 600, 660, "Lecture"),
                False,
            ),
            (
                Block(["M"], 540, 600, "Lecture"),
                Block(["T"], 570, 630, "Lecture"),
                False,
            ),
            (
                Block(["M"], 540, 660, "Lecture"),
                Block(["M"], 570, 600, "Section"),
                True,
            ),
            (
                Block([], 540, 600, "Lecture"),
                Block(["M"], 570, 630, "Lecture"),
                False,
            ),
        ]

        for block_a, block_b, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(time_conflicts(block_a, block_b), expected)

    def test_option_conflicts(self):
        option_a = [
            Block(["M"], 540, 590, "Lecture"),
            Block(["F"], 540, 590, "Section"),
        ]
        safe_option = [
            Block(["M"], 600, 650, "Lecture"),
            Block(["F"], 600, 650, "Section"),
        ]
        conflicting_option = [
            Block(["M"], 570, 630, "Lecture"),
            Block(["R"], 600, 650, "Section"),
        ]

        self.assertFalse(option_conflicts(option_a, safe_option))
        self.assertTrue(option_conflicts(option_a, conflicting_option))


class TestCourse(unittest.TestCase):
    def test_create_options(self):
        lectures = [
            Block(["M"], 540, 590, "Lecture"),
            Block(["T"], 540, 590, "Lecture"),
        ]
        sections = [
            Block(["W"], 600, 650, "Section"),
            Block(["R"], 600, 650, "Section"),
        ]

        course = Course("Test", "TEST", lectures, sections)
        self.assertEqual(len(course.create_options()), 4)

    def test_lecture_only_course(self):
        lecture = Block(["M"], 540, 590, "Lecture")
        course = Course("Lecture Only", "ONLY", [lecture], [])

        self.assertEqual(course.create_options(), [[lecture]])

    def test_print_course(self):
        lecture = Block(["M"], 540, 590, "Lecture")
        course = Course("Demo", "D1", [lecture], [])

        output = io.StringIO()

        with redirect_stdout(output):
            course.print_course()

        self.assertIn("Demo (D1)", output.getvalue())


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.math1 = Block(["M", "W"], 540, 590, "Lecture")
        self.math2 = Block(["T", "R"], 660, 735, "Lecture")
        self.math_section = Block(["F"], 540, 590, "Section")

        self.cs1 = Block(["M", "W"], 600, 650, "Lecture")
        self.cs2 = Block(["T", "R"], 690, 765, "Lecture")
        self.cs_section = Block(["F"], 600, 650, "Section")

        self.music_lecture = Block(["M", "W"], 780, 830, "Lecture")
        self.music_section = Block(["F"], 780, 830, "Section")

        self.writing_lecture = Block(["T", "R"], 840, 915, "Lecture")
        self.writing_section = Block(["W"], 840, 890, "Section")

        self.math = Course(
            "Math", "MATH",
            [self.math1, self.math2],
            [self.math_section],
        )
        self.cs = Course(
            "Computer Science", "CS",
            [self.cs1, self.cs2],
            [self.cs_section],
        )
        self.music = Course(
            "Music", "MUS",
            [self.music_lecture],
            [self.music_section],
        )
        self.writing = Course(
            "Writing", "WRIT",
            [self.writing_lecture],
            [self.writing_section],
        )

        self.scheduler = Scheduler(
            [self.math, self.cs, self.music, self.writing]
        )

        self.valid_schedule = (
            self.math.create_options()[0],
            self.cs.create_options()[0],
            self.music.create_options()[0],
            self.writing.create_options()[0],
        )

        self.invalid_schedule = (
            self.math.create_options()[1],
            self.cs.create_options()[1],
            self.music.create_options()[0],
            self.writing.create_options()[0],
        )

    def test_generate_schedules(self):
        output = io.StringIO()

        with redirect_stdout(output):
            self.scheduler.generate_schedules()

        result = output.getvalue()

        self.assertIn("Expected raw schedules: 4", result)
        self.assertIn("Actual raw schedules: 4", result)
        self.assertIn("Valid schedules: 3", result)

    def test_schedule_is_valid(self):
        self.assertTrue(self.scheduler.schedule_is_valid(self.valid_schedule))
        self.assertFalse(self.scheduler.schedule_is_valid(self.invalid_schedule))
        self.assertTrue(self.scheduler.schedule_is_valid(()))

    def test_get_all_schedule_blocks(self):
        blocks = self.scheduler.get_allScheduleBlocks(self.valid_schedule)
        self.assertEqual(len(blocks), 8)

    def test_sort_by_days(self):
        days = self.scheduler.sort_by_days(self.valid_schedule)

        self.assertEqual(len(days), 5)
        self.assertEqual(
            [block.startTime for block in days[0]],
            [540, 600, 780],
        )
        self.assertEqual(
            [block.startTime for block in days[2]],
            [540, 600, 780, 840],
        )

    def test_score_days(self):
        score = self.scheduler.score_days(
            self.valid_schedule,
            ["M", "W", "F"],
        )
        self.assertAlmostEqual(score, 10 / 12)

    def test_score_time_range(self):
        score = self.scheduler.score_timeRange(
            self.valid_schedule,
            600,
            840,
        )
        self.assertAlmostEqual(score, 6 / 12)

    def test_score_gap(self):
        score = self.scheduler.score_gap(self.valid_schedule, 60)
        self.assertAlmostEqual(score, 4 / 7)

    def test_score_schedule(self):
        preferences = {
            "preferredDays": ["M", "W", "F"],
            "preferredStart": 600,
            "preferredEnd": 840,
            "preferredGap": 60,
            "dayWeight": 1,
            "timeWeight": 2,
            "gapWeight": 3,
        }

        expected = ((10 / 12) + (6 / 12 * 2) + (4 / 7 * 3)) / 6 * 100

        score = self.scheduler.score_schedule(
            self.valid_schedule,
            preferences,
        )

        self.assertAlmostEqual(score, expected)


if __name__ == "__main__":
    unittest.main()