"""Seed data from SRS v3.3: STEM pathway (3.4), levels and subjects (3.1-3.3), Term Classes
fees (FR-PAY-01), Holiday Tuition sessions and fees (3.6, FR-PAY-01) and tertiary packages (3.5).
The Admin edits all of it from the back-office."""

from decimal import Decimal

from django.db import migrations

PATHWAY = [
    (
        "Lower Primary",
        "Numbers, shapes, measurement, money, simple data with pictograms",
        "Living things, materials, weather, simple experiments, PhET basics",
        "Unplugged coding, Scratch Jr, mouse and keyboard skills, safe internet",
        "Build-and-make activities inside Science",
    ),
    (
        "Upper Primary",
        "Fractions, decimals, percentages, geometry, word problems; Common Entrance and First "
        "School Leaving Examination preparation",
        "Basic Science: energy, the human body, simple machines, experiments",
        "Scratch, micro:bit, MS Word and PowerPoint, typing, digital citizenship",
        "Simple machines projects",
    ),
    (
        "Junior Secondary",
        "Algebra, geometry, statistics with spreadsheets; BECE preparation",
        "Basic Science; virtual labs; BECE preparation",
        "Python basics, Arduino introduction, Excel/Google Sheets, digital productivity",
        "Computer Hardware and GSM Repairs; Basic Technology projects",
    ),
    (
        "Senior Secondary",
        "Mathematics and Further Mathematics; WAEC, NECO and JAMB preparation; Python for maths",
        "Physics, Chemistry, Biology with simulations and sensors; WAEC, NECO and JAMB "
        "preparation",
        "Python, web basics, data with spreadsheets, IoT/robotics (Art stream: productivity, "
        "CorelDraw, web basics, digital marketing basics)",
        "Computer Hardware and GSM Repairs (both streams); Introduction to Robotics (Science "
        "stream)",
    ),
    (
        "Tertiary",
        "Mathematics and Statistics (engineering maths, calculus, numerical function, Laplace "
        "transform)",
        "Applied science support",
        "Tertiary packages",
        "IoT/Robotics, GSM/Mobile Repairs and engineering projects",
    ),
]

LEVELS = [
    (
        "primary",
        "Lower Primary",
        "lower-primary",
        "Primary 1, 2 and 3 (Junior Primary)",
        "6 to 8",
        "",
        "Lower Primary",
        "30000",
        [
            ("Mathematics", "with fun maths games"),
            ("Science", "simulations and science games"),
            ("Coding/Digital Technologies", "ScratchJr and Scratch 3"),
            ("Fun STEM Projects", ""),
        ],
    ),
    (
        "primary",
        "Upper Primary",
        "upper-primary",
        "Primary 4, 5 and 6",
        "9 to 11",
        "Common Entrance and First School Leaving Examination",
        "Upper Primary",
        "30000",
        [("Mathematics", ""), ("Science", ""), ("Coding/Digital Technologies", "")],
    ),
    (
        "secondary",
        "Junior Secondary",
        "junior-secondary",
        "JSS 1, 2 and 3",
        "11 to 14",
        "BECE",
        "Junior Secondary",
        "30000",
        [
            ("Mathematics", ""),
            ("Basic Science", ""),
            ("Coding/Digital Technologies", ""),
            ("Computer Hardware and GSM Repairs", ""),
        ],
    ),
    (
        "secondary",
        "Senior Secondary Science",
        "senior-secondary-science",
        "SS 1, 2 and 3, Science stream",
        "14 to 17",
        "WAEC, NECO and JAMB/UTME",
        "Senior Secondary",
        "40000",
        [
            ("Mathematics/Further Mathematics", ""),
            ("Physics", ""),
            ("Chemistry", ""),
            ("Biology", ""),
            (
                "Coding/Digital Technologies",
                "including Introduction to Robotics and Competitive/Dynamic Programming",
            ),
            ("Computer Hardware and GSM Repairs", ""),
        ],
    ),
    (
        "secondary",
        "Senior Secondary Art",
        "senior-secondary-art",
        "SS 1, 2 and 3, Art stream",
        "14 to 17",
        "WAEC, NECO and JAMB/UTME",
        "Senior Secondary",
        "30000",
        [
            ("Mathematics/Further Mathematics", ""),
            (
                "Coding/Digital Technologies",
                "computer knowledge, programming, web development and data analysis",
            ),
            ("Computer Hardware and GSM Repairs", ""),
        ],
    ),
]

HOLIDAY_SESSIONS = [("Easter/April", "40000"), ("Summer/August", "60000"), ("December", "20000")]

PACKAGES = [
    ("Computer Programming", "computer-programming",
     "Python, JavaScript and C/C++ fundamentals, problem solving", "Online / Hybrid"),
    ("Computer Basics", "computer-basics",
     "MS Word/Google Docs, Excel/Google Sheets, PowerPoint, CorelDraw",
     "Online / On-site / Hybrid"),
    ("Digital Productivity Tools", "digital-productivity-tools",
     "Google Workspace, cloud storage, email, collaboration and AI productivity tools", "Online"),
    ("Creative Digital Skills", "creative-digital-skills",
     "Graphic design, video editing, content creation", "Online / Hybrid"),
    ("Web Development", "web-development",
     "HTML, CSS, JavaScript, Python/Django, deployment", "Online / Hybrid"),
    ("IoT / Robotics", "iot-robotics",
     "Arduino, ESP32, sensors, actuators, IoT dashboards", "Hybrid (practicals on-site)"),
    ("Data Analysis / Analytics", "data-analysis",
     "Excel, SQL, Python, dashboards", "Online"),
    ("Machine Learning", "machine-learning",
     "Python, scikit-learn, introduction to deep learning", "Online"),
    ("Digital Marketing", "digital-marketing",
     "Social media, SEO, paid ads, analytics", "Online"),
    ("GSM / Mobile Repairs", "gsm-mobile-repairs",
     "Phone hardware, diagnostics, software flashing", "On-site / Hybrid (practicals on-site)"),
    ("Cybersecurity", "cybersecurity",
     "Security fundamentals, networking, ethical hacking basics", "Online / Hybrid"),
    ("Mathematics and Statistics", "mathematics-and-statistics",
     "Engineering maths, calculus, numerical function, Laplace transform", "Online / On-site"),
]


def seed(apps, schema_editor):
    PathwayStage = apps.get_model("programmes", "PathwayStage")
    Level = apps.get_model("programmes", "Level")
    LevelSubject = apps.get_model("programmes", "LevelSubject")
    HolidaySession = apps.get_model("programmes", "HolidaySession")
    TertiaryPackage = apps.get_model("programmes", "TertiaryPackage")

    stages = {}
    for order, (name, maths, science, coding, hardware) in enumerate(PATHWAY, start=1):
        stages[name] = PathwayStage.objects.create(
            order=order, name=name, mathematics=maths, science=science, coding=coding,
            hardware=hardware,
        )
    for order, (group, name, slug, classes, ages, exams, stage, fee, subjects) in enumerate(
        LEVELS, start=1
    ):
        level = Level.objects.create(
            order=order, group=group, name=name, slug=slug, classes=classes, ages=ages,
            exams=exams, stage=stages[stage], term_fee=Decimal(fee),
        )
        for position, (subject, detail) in enumerate(subjects, start=1):
            LevelSubject.objects.create(level=level, order=position, name=subject, detail=detail)
    for order, (name, fee) in enumerate(HOLIDAY_SESSIONS, start=1):
        HolidaySession.objects.create(order=order, name=name, fee=Decimal(fee))
    for order, (name, slug, focus, delivery) in enumerate(PACKAGES, start=1):
        TertiaryPackage.objects.create(
            order=order, name=name, slug=slug, focus=focus, delivery=delivery
        )


class Migration(migrations.Migration):
    dependencies = [("programmes", "0001_initial")]

    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
