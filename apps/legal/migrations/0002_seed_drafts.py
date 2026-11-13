"""Draft legal pages written from the rules in SRS v3.3. They are drafts for the Project Owner and
a legal reviewer (v3.3 Appendix B item 22) and show an 'under review' notice until approved."""

from django.db import migrations

PAGES = [
    (
        "privacy",
        "Privacy Policy",
        "How OCEANZ STEM HUB collects, uses and protects personal information.",
        """## Who we are
OCEANZ STEM HUB, #5 Gunning Rd, Abakaliki, Ebonyi State, Nigeria, is responsible for the personal information described in this policy. You can reach us through the details on our Contact page.

## What we collect
- When you send an enquiry or use the contact form: your name, email address, phone and WhatsApp number, country, your child's class, the tutoring option and delivery format you prefer, and your message.
- When you express interest in teaching: your name, email address, WhatsApp number and the subjects you teach.
- Technical information needed to run the website securely, such as your IP address, which we use to prevent spam and abuse.

## Why we use it
- To reply to your enquiry and arrange classes or free trial classes.
- To contact people interested in teaching with us.
- To keep the website secure.
We do not use children's information for marketing.

## Legal basis
We process personal information in line with the Nigeria Data Protection Act 2023, on the basis of your consent and of the steps needed to answer your request.

## Who we share it with
We use trusted service providers to run the website: our hosting provider, our email provider, and Cloudflare Turnstile, which checks that forms are sent by people. They process information only to provide their service to us. We do not sell personal information.

## How long we keep it
We keep enquiries for up to 2 years and then delete or anonymise them.

## Children
Information about learners under 18 is given to us by their parent or guardian.

## Your rights
You may ask to see, correct or delete your personal information, or withdraw your consent, by contacting us. You may also complain to the Nigeria Data Protection Commission.

## Changes
We update this policy when our services change. The version and date are shown on this page.""",
    ),
    (
        "terms",
        "Terms of Service",
        "The terms for registration, classes and fees at OCEANZ STEM HUB.",
        """## About these terms
These terms apply to registration and classes with OCEANZ STEM HUB.

## Registration
- Registration is per term.
- A one-time, non-refundable registration fee is paid per child before the registration form.
- A parent or guardian registers learners under 18.

## Classes and fees
- We confirm each learner's class before any programme fee is due. The programme fee is invoiced only when the class is confirmed to run.
- Fees are paid in full, once, before classes begin. There are no instalments.
- Private tutoring is priced by quote and paid once a month, in advance.
- Fees are not refundable after payment. Please read our No-Refund Policy.
- A sibling discount applies to programme fees for the second and further children registered by the same parent or guardian for the same term. It does not apply to the registration fee.

## Learning requirements
For online lessons the learner needs a computer or smart device, reliable internet, a quiet learning space and learning materials.

## Conduct
Learners, parents and teachers commit to Consistency, Competence and Character, follow class rules and the Academic Integrity Policy, and treat everyone with respect.

## Safeguarding and recordings
Our Child Protection and Safeguarding Policy and our Recording Policy form part of these terms.

## Changes
We may update these terms. The latest version is always published on this page.""",
    ),
    (
        "no-refund-policy",
        "No-Refund Policy",
        "Fees paid to OCEANZ STEM HUB are not refundable. This page explains what happens instead.",
        """## Our policy
All fees paid to OCEANZ STEM HUB, including the registration fee, programme fees and private tutoring fees, are not refundable once paid.

## Before you pay
- We invoice a programme fee only after we confirm your child's class will run.
- Please read the class details, timetable and requirements before paying.

## If OCEANZ cancels a class
If we cancel a class that is already running, the amount you paid becomes credit for the next term, or is moved to another class or delivery format that we agree with you.

## Changing class or format
If, with our approval, you switch between a class place and private tutoring or change delivery format during a term, any difference is invoiced or held as credit.

## Your rights
This policy does not affect any rights you have under Nigerian consumer protection law.""",
    ),
    (
        "safeguarding",
        "Child Protection and Safeguarding Policy",
        "How OCEANZ STEM HUB keeps children safe in every lesson, online, on-site and at home.",
        """## Our commitment
The safety and wellbeing of every child comes first at OCEANZ STEM HUB.

## Safer recruitment
Every teacher is verified (identity, qualifications, references and TRCN registration where it applies), interviewed or trained by the OCEANZ Teacher Academy, and agrees to our child-safeguarding code of conduct before teaching.

## Safe communication
- Teachers do not message learners under 18 privately. They communicate in class or group spaces, or in conversations that include the parent or guardian.
- Group and class discussions are visible to the supervising teacher and the Admin.

## Online lessons
- One-on-one online lessons with children are always recorded.
- Parents and guardians may observe their child's live lessons.
- Children appear by first name only.

## Home lessons
Home lessons are given only by verified teachers, only within our service area, and with a parent, guardian or other responsible adult at home throughout. Each visit is logged.

## Photos and personal details
We do not publish photos of children or their full names without the consent of their parent or guardian.

## Reporting a concern
If you are worried about a child's safety, contact our Safeguarding Lead through the details on our Contact page. If a child is in immediate danger, contact the police.""",
    ),
    (
        "academic-integrity",
        "Academic Integrity Policy",
        "Our rules for honest work in quizzes, exams, homework and projects.",
        """## Honest work
Learners complete quizzes, exams, homework and projects themselves, without copying, sharing answers or asking someone else to do the work.

## Quizzes and exams
- Quizzes and exams are taken in the browser, and the rules are shown before each one starts.
- During term exams, leaving the exam page, for example by switching tabs or apps, ends the attempt, which a teacher then reviews.
- Copying, pasting and printing are switched off during assessments.

## Projects
Ideas and help from others may be used in projects only when they are credited.

## Consequences
Breaking these rules may lead to a score of zero, a repeated assessment or other action decided by the teacher and the Admin. Parents and guardians are informed.""",
    ),
    (
        "cookie-policy",
        "Cookie Policy",
        "The cookies and similar technologies the OCEANZ STEM HUB website uses.",
        """## Cookies we use
We use only the cookies the website needs to work:
- A security cookie that protects our forms against misuse (csrftoken).
- A session cookie that remembers your progress through a form, such as your enquiry reference (sessionid).

## Choices saved on your device
Your theme choice and any notices you close are saved in your browser's local storage. They are not sent to us.

## Third-party services
- Cloudflare Turnstile checks that forms are sent by people.
- The map on our Contact page is provided by Google Maps and loads only when you choose to show it. Google may then set its own cookies.

## Managing cookies
You can delete or block cookies in your browser settings. Blocking the essential cookies may stop our forms from working.""",
    ),
    (
        "recording-policy",
        "Recording Policy",
        "When OCEANZ STEM HUB records lessons, who can watch the recordings and how long they are kept.",
        """## What we record
- Live classes may be recorded so that learners can catch up, for example after losing power or data.
- One-on-one online lessons with learners under 18 are always recorded, for safeguarding.

## Who can watch recordings
Recordings play only inside the OCEANZ website, for learners enrolled in the class, their parents or guardians, their teachers and the Admin. Each recording shows the viewer's name as a watermark.

## How long we keep them
Recordings are deleted after 12 months.

## Sharing
Recordings must not be downloaded, copied or shared outside the OCEANZ website.""",
    ),
]


def seed(apps, schema_editor):
    LegalPage = apps.get_model("legal", "LegalPage")
    for slug, title, summary, body in PAGES:
        LegalPage.objects.get_or_create(
            slug=slug, defaults={"title": title, "summary": summary, "body": body}
        )


class Migration(migrations.Migration):
    dependencies = [("legal", "0001_initial")]

    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
