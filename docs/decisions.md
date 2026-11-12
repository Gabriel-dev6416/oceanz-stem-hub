# OCEANZ STEM HUB - Decisions on top of SRS v3.1

These decisions were agreed with the Project Owner on 12 November 2026 after the review of
SRS v3.1. Where they differ from the SRS, this file takes precedence until the SRS is reissued.

## Curriculum basis

All class, subject and topic seed data follows the standard Nigerian school curriculum
(NERDC Basic Education Curriculum for Primary and JSS; NERDC Senior Secondary curriculum for
SS 1-3), mapped to Common Entrance, BECE, WAEC, NECO and JAMB. Seed data stays editable by the
Admin from the back-office.

## D-01 Curriculum explorer in R1

FR-ENG-01 ships in R1. A simple curriculum topics table (class, subject, term, week, topic,
learning objectives) is built in R1 and edited by the Admin. R3 extends the same table with
syllabus mapping, teacher proposals and the curriculum tracker (FR-ACD-05, FR-PRG-05).

## D-02 Free trial button before R3

Until trial booking (FR-ENG-02) ships in R3, every "Book a Free Trial Class" button opens the
enquiry form with the enquiry type "Free trial class" pre-selected, with WhatsApp beside it.
R3 replaces the target with the booking flow; the buttons themselves do not change.

## D-03 Homepage blocks hidden until real content exists

"Meet our teachers", teacher intro videos, testimonials, results statistics, partners and the
"Built at OCEANZ" showcase render only when the Admin has published at least one real item.
No placeholder content is ever shown.

## D-04 Weekly report moves to Monday

The weekly quiz window stays Friday 08:00 to Sunday 20:00. The weekly progress report
(FR-PRG-03) is generated on Monday at 08:00 (configurable) and covers the previous Monday to
Sunday, so it always includes that week's quiz. The home challenge is sent with it.

## D-05 Strict exam mode grace period

FR-CBT-15 default grace period changes from 0 seconds to 3 seconds (configurable 0-5 s per
exam), so a notification, incoming call or screen dimming on a low-end phone does not suspend
the attempt.

## D-06 Strict exam mode on iOS

Safari on iPhone cannot put a web page into full screen. On iOS the full-screen requirement is
dropped; leaving the page is detected through page visibility, page hide and window blur,
with the same grace period. All other Strict rules apply unchanged.

## D-07 Junior Primary small groups by year

Junior Primary (Primary 1-3) remains one class with one dashboard. The "Split class" proposal
(FR-GRP-02) forms small groups by year (Primary 1, 2 and 3) by default; mixing years in a
group needs a recorded reason. Curriculum topics and weekly quizzes are set per year.

## D-08 Sibling discount order

For each guardian and term, enrolments are ordered by fee, highest first. The highest pays
full price; the sibling discount (default 10%) applies to every other enrolment.

## D-09 Senior Secondary Commercial stream

Senior Secondary gets a third stream, Commercial, alongside Science and Art, as in the Nigerian
SS curriculum. Seed classes: SS 1-3 Commercial. Subjects offered by OCEANZ: Mathematics and
Coding/Digital Technologies (with emphasis on spreadsheets, data and digital business tools).

## D-10 On-site drop-off and pick-up

New requirement FR-SAF-08 (Must, R3): for on-site sessions with minors, the guardian registers
approved pick-up persons. Drop-off is recorded on the register; at pick-up the collecting
adult gives the guardian's pick-up PIN, which is checked and logged. A failed check alerts the
Safeguarding Lead and the guardian.

## D-11 Teacher earnings module

New later module (R6): teacher earnings, computed from attendance-verified sessions,
allocations and private tutoring hours, with payslips and Finance Officer approval. Pay rates
and rules need a separate Owner decision before design.

## D-12 Technical notes adopted

- Zoom: every learner joins with their platform ID as the Meeting SDK `customerKey`, so
  attendance webhooks map to learners without relying on display names.
- Watermarks are a deterrent and make leaks traceable; Bunny Stream DRM is an option if leaks
  occur.
- Notes conversion (Word, PowerPoint to watermarked page images) uses LibreOffice inside the
  Docker image, so the application is deployed to Render as a Docker image.
- A monthly running-cost budget (Render, Zoom licences, Bunny, email, SMS, AI) is agreed in R0.

## D-13 Corrections

- FR-PRG-03: "topics covered topics for next week" reads "topics covered and topics for next
  week".
