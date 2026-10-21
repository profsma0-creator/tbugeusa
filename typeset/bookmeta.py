"""Bibliographic and structural metadata for the textbook."""

TITLE = "Advanced Assessment and Diagnosis"
SUBTITLE = "A Doctoral-Level Textbook in Counselling Psychology"
COURSE = "CPY 903"
IMPRINT = "Triune Biblical University Global Extension, USA"
IMPRINT_SUB = "Online University, Shirley, New York, USA"
IMPRINT_URL = "www.tbuglobalextensionusa.com"
EDITION = "First edition"
AUTHOR = "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA"
PLACE = "New York, USA"
# The corporate author and the publisher are the same institution, so the
# title page carries the name once, as author, and the city at the foot.

# Running-head title (verso pages)
RUNNING_TITLE = "Advanced Assessment and Diagnosis"

# Editorial placeholders that require author or publisher input.
AIR_MARK = "[AUTHOR TO SUPPLY]"  # no longer used: author supplied by publisher

PARTS = [
    ("PART I", "Foundations and Measurement",
     "The purposes of assessment, the logic of clinical inference, interviewing, "
     "and the psychometric basis of score interpretation.", [1, 2, 3, 4]),
    ("PART II", "Assessing Dispositions and Abilities",
     "Personality and interpersonal functioning, cognitive and neuropsychological "
     "ability, and achievement, aptitude and career assessment.", [5, 6, 7]),
    ("PART III", "Assessing Clinical Presentations",
     "Mood, anxiety, obsessive-compulsive, trauma-related, bipolar, psychotic, "
     "substance-related and enduring personality presentations.", [8, 9, 10, 11]),
    ("PART IV", "Development, Culture and Relational Systems",
     "Children and adolescents, couples and families, and the cultural, linguistic "
     "and disability considerations that condition every interpretation.", [12, 13, 14]),
    ("PART V", "Risk, Integration and Communication",
     "Risk assessment and safeguarding, and the integration of multimethod evidence "
     "into formulation, reports and feedback.", [15, 16]),
]

# Short running-head titles for chapters ("CHAPTER 1" is added by the typesetter)
SHORT_TITLES = {
    1: "Foundations of Assessment and Diagnosis",
    2: "Clinical Interviewing and Diagnostic Reasoning",
    3: "Psychometrics",
    4: "Test Selection and Interpretation",
    5: "Personality Assessment",
    6: "Cognitive and Neuropsychological Assessment",
    7: "Achievement, Aptitude and Career Assessment",
    8: "Mood, Anxiety and Trauma-Related Problems",
    9: "Bipolar and Psychotic Disorders",
    10: "Personality Disorders",
    11: "Substance Use and Behavioural Addictions",
    12: "Child and Adolescent Assessment",
    13: "Couples and Family Assessment",
    14: "Culture, Language, Disability and Fairness",
    15: "Risk Assessment and Safeguarding",
    16: "Integration, Reporting and Feedback",
}

# Words spelled in American English in the source that are normalised to
# British English by the copy-editing pass (kept here for transparency).
SPELLING_NOTE = (
    "British English spelling has been applied throughout "
    "(e.g. behaviour, organisation, judgement, programme, recognised, "
    "standardised). Proper names and the titles of published instruments, "
    "organisations and works retain their original spelling."
)
