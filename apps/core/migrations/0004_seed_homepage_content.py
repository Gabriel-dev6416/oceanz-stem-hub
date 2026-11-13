"""Homepage seed content from SRS v3.3.

Feature cards are the four named in FR-WEB-01. FAQs are unpublished drafts written from facts
in SRS v3.3 for the Project Owner to review, edit and publish (v3.3 Appendix B item 25).
"""

from django.db import migrations

FEATURES = [
    (
        "live",
        "Live online classes",
        "Learners join live lessons inside the OCEANZ website, with no meeting links to share.",
    ),
    (
        "on-site",
        "On-site Saturdays",
        "Hands-on lessons every Saturday at our hub, #5 Gunning Rd, Abakaliki.",
    ),
    (
        "verified",
        "Verified teachers",
        "Every teacher is interviewed or Academy-trained, verified and safeguarding-trained.",
    ),
    (
        "reports",
        "Weekly reports to parents",
        "Quiz results, attendance and a teacher's comment sent to parents every week.",
    ),
]

FAQ_DRAFTS = [
    (
        "Who can learn at OCEANZ STEM HUB?",
        "Primary, Secondary (JSS and SS Science or Art) and Tertiary learners, in Nigeria and "
        "abroad.",
    ),
    (
        "How much is registration?",
        "Registration is a one-time fee of ₦1,000 per child, paid before the registration form. "
        "It is not refundable.",
    ),
    (
        "Can my child learn from home?",
        "Yes. Learners can join live online classes from home, or have home lessons after school "
        "and at weekends within Abakaliki, with a verified teacher and an adult at home.",
    ),
    (
        "What does my child need for online classes?",
        "A computer or smart device, reliable internet, a quiet learning space and learning "
        "materials. Learners without these can attend on-site at the hub.",
    ),
    (
        "Do you offer one-on-one lessons?",
        "Yes. Private tutoring is priced by quote and paid once a month in advance. Contact us "
        "for a quote.",
    ),
]


def seed(apps, schema_editor):
    FeatureCard = apps.get_model("core", "FeatureCard")
    FAQ = apps.get_model("core", "FAQ")
    if not FeatureCard.objects.exists():
        for order, (icon, title, text) in enumerate(FEATURES, start=1):
            FeatureCard.objects.create(order=order, icon=icon, title=title, text=text)
    if not FAQ.objects.exists():
        for order, (question, answer) in enumerate(FAQ_DRAFTS, start=1):
            FAQ.objects.create(order=order, question=question, answer=answer, published=False)


class Migration(migrations.Migration):
    dependencies = [("core", "0003_homepage_content")]

    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
