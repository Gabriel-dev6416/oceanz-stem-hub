"""Classes of the Nigerian school system (SRS v3.3 section 3.1).

Primary 1-3 are listed separately for parents and form the Junior Primary class. R2 replaces
this list with the Admin-managed classes.
"""

CLASS_CHOICES = [
    (
        "Primary",
        [(f"primary-{year}", f"Primary {year}") for year in range(1, 7)],
    ),
    (
        "Secondary",
        [
            ("jss-1", "JSS 1"),
            ("jss-2", "JSS 2"),
            ("jss-3", "JSS 3"),
            ("ss-1-science", "SS 1 Science"),
            ("ss-1-art", "SS 1 Art"),
            ("ss-2-science", "SS 2 Science"),
            ("ss-2-art", "SS 2 Art"),
            ("ss-3-science", "SS 3 Science"),
            ("ss-3-art", "SS 3 Art"),
        ],
    ),
    ("Tertiary", [("tertiary", "Tertiary package")]),
]
CLASS_LEVELS = {value: group for group, options in CLASS_CHOICES for value, _ in options}
CLASS_NAMES = {value: name for _, options in CLASS_CHOICES for value, name in options}
SCHOOL_CLASS_CHOICES = [group for group in CLASS_CHOICES if group[0] != "Tertiary"]


def level_slug(class_code):
    """The programme level page a class belongs to, e.g. 'jss-2' -> 'junior-secondary'."""
    if class_code.startswith("primary-"):
        return "lower-primary" if int(class_code[-1]) <= 3 else "upper-primary"
    if class_code.startswith("jss-"):
        return "junior-secondary"
    if class_code.startswith("ss-"):
        return f"senior-secondary-{class_code.rsplit('-', 1)[1]}"
    return ""
