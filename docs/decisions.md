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

## D-14 Editing website content in R1

Until the branded staff back-office (/staff/) and the Admin and staff roles arrive in R2, the
owner edits site settings and homepage content in the Django admin at the private admin path.
R2 moves this editing into /staff/ and limits the Django admin to Super Admins (FR-ADM-01).

## D-15 Logo

The header shows the text wordmark "OCEANZ STEM HUB" until the official logo file is supplied.

## D-16 SRS review fixes (12 November 2026)

1. **Class place, not "group".** Parents buy a Class place or Private tutoring; small groups sit
   inside a class. FR-PAY-01, FR-PVT-09, FR-WEB-05 and the Section 17 enrolment scenario read
   "class place" (or "Class/Private") wherever they say "group". Fee structures, the pricing
   page and enrolment screens use this wording.
2. **No class capacity.** The "capacity" field is removed from classes (FR-ACD-02). Classes have
   a minimum to open (default 12, FR-ACD-09) and no maximum. Capacity exists only on tertiary
   cohorts, holiday programmes and the on-site venue, which drive the waitlist (FR-ENR-09).
3. **Finance conflict of interest is Must, R2.** SEC-ACL-04 is split: a Finance Officer cannot
   verify payments or approve refunds for themselves or for families of learners they teach
   (Must, R2, same as FR-STF-04 and the Section 14.1 test case). The second approver for a
   teacher's own learners' term results stays Should, R4.
4. **Free trial button before R3.** Already decided in D-02: it opens the enquiry form with
   "Free trial class" pre-selected until trial booking ships in R3.
5. **Recordings follow retention; notes and lesson videos are archived.** FR-PRT-08 applies to
   notes and uploaded lesson videos: archived, never deleted, when learners lose access. Live
   class recordings follow FR-LIV-11 and SEC-LIV-04: deleted after the retention period
   (default 12 months).
6. **FR-PRG-03 wording.** Already corrected in D-13: "teacher comment, topics covered, topics
   for next week".
