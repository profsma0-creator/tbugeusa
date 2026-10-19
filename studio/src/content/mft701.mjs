// MFT 701 — Fundamentals of Marriage and Family Therapy
// Sixteen-week graduate seminar. Content authored for the deck.

const course = {
  code: 'MFT 701',
  title: 'Fundamentals of Marriage and Family Therapy',
  subtitle: 'A Sixteen-Week Graduate Seminar',
  coverLine: 'Theory  ·  Practice  ·  Supervision  ·  Professional Identity',
  semester: 'First Semester',
  units: '1.71',
  slideCount: 0,

  description:
    'This course introduces marriage and family therapy as a distinctive discipline: a way of understanding distress as it is produced, maintained and transformed in relationships. Students encounter the field’s intellectual history, its major theoretical traditions, and the practical and ethical demands of clinical work with couples and families. The emphasis throughout is on systemic thinking — learning to see patterns, contexts and meanings rather than isolated symptoms.',

  aims: [
    'Establish a systemic vocabulary for describing relational problems.',
    'Map the major models of family therapy and their points of divergence.',
    'Practise core clinical skills: joining, assessment, formulation, intervention.',
    'Locate practice within ethical, cultural and legal frameworks.',
    'Begin a reflective professional identity grounded in evidence and supervision.',
  ],

  distinct: [
    'The relational system, not the individual, is the unit of assessment.',
    'Symptoms are understood as maintained by current interaction, not only by history.',
    'The therapist is a participant in the system, not an external observer.',
    'Change is evaluated in relationships — and through the client’s own feedback.',
  ],

  outcomes: [
    'Explain the systemic epistemology that distinguishes MFT from individually oriented psychotherapy.',
    'Compare the major models of family therapy — structural, strategic, intergenerational, experiential, cognitive-behavioural, solution-focused and narrative.',
    'Conduct a first session: join a multi-person system, negotiate consent, and elicit each member’s description of the problem.',
    'Construct a three-generation genogram and use circular questioning to assess relational patterns.',
    'Formulate a case systemically, integrating developmental, cultural, ethical and risk considerations.',
    'Use routine outcome monitoring and reflective practice to evaluate and improve your own clinical work.',
  ],

  rhythm: [
    { title: 'Read', body: 'Two set readings frame the week. Read for argument, not coverage: what does this model see, and what does it miss?', time: 'Before the lecture' },
    { title: 'Wrestle', body: 'The lecture introduces the model and its clinical logic. Expect to compare it with the models already in the room.', time: 'Lecture · 2 hours' },
    { title: 'Practise', body: 'Seminar and skills lab: role-play, live supervision, genogram construction, case formulation in small groups.', time: 'Seminar · 2 hours' },
    { title: 'Reflect', body: 'A weekly journal entry: what did this week ask of you, personally and professionally?', time: 'Journal · 20 minutes' },
  ],

  assessment: [
    ['Integrative case formulation', '2,500 words · one family, three models, a defended intervention plan', '30%'],
    ['Seminar participation', 'Prepared contribution, role-play, peer feedback', '15%'],
    ['Mid-semester examination', 'Short answers and a seen case', '20%'],
    ['Final examination', 'Essay questions across the full syllabus', '35%'],
  ],

  phases: [
    {
      roman: 'I', name: 'Foundations', range: '1–4', start: 1, end: 4,
      blurb: 'Learning to see systems: the history, the cybernetic grammar, and the first maps of family structure.',
      weeks: ['What is MFT?', 'Cybernetics & the systemic lens', 'A short history of the field', 'Structural & strategic foundations'],
    },
    {
      roman: 'II', name: 'Theoretical Cartography', range: '5–8', start: 5, end: 8,
      blurb: 'The major traditions, held side by side — intergenerational, experiential, postmodern, and the discipline of integration.',
      weeks: ['Intergenerational & contextual', 'Experiential & humanistic', 'Postmodern & constructivist', 'Integrative formulation'],
    },
    {
      roman: 'III', name: 'The Clinical Encounter', range: '9–12', start: 9, end: 12,
      blurb: 'Joining, assessing and negotiating the ethical and cultural complexity of real clinical work.',
      weeks: ['First session & alliance', 'Assessment & genograms', 'Ethics, law & governance', 'Culture, power & location'],
    },
    {
      roman: 'IV', name: 'Integration & Transition', range: '13–16', start: 13, end: 16,
      blurb: 'Applying systemic thinking across the life course, and beginning the transition to supervised practice.',
      weeks: ['Children & adolescents', 'Couples & attachment', 'Transitions & crisis', 'Evidence & professional identity'],
    },
  ],

  weeks: [
    // ── WEEK 1 ──────────────────────────────────────────────────────────────
    {
      n: 1, phase: 0,
      title: 'What Is Marriage and Family Therapy?',
      question: 'When the unit of treatment is a relationship, what exactly is it that changes?',
      outcomes: [
        'Distinguish systemic practice from individually oriented psychotherapy.',
        'Describe the relational unit of treatment and its implications.',
        'Begin a personal statement of professional identity.',
      ],
      terms: ['systemic epistemology', 'relational unit', 'presenting problem', 'professional identity'],
      reading: 'Key reading · Nichols & Davis (2020), ch. 1 · Becvar & Becvar (2018), ch. 1',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 01',
          title: 'The relational unit of treatment',
          lead: 'MFT begins from a deceptively simple claim: problems are not located only inside people. They are located in the patterns between people.',
          blocks: [
            {
              h: 'A different unit of analysis',
              body: 'Individual therapy treats the person as the locus of difficulty. MFT treats the relationship as the client — the recurring patterns that organise how family members think, feel and act.',
              items: ['The symptom is also a message about the system', 'Assessment includes the family’s own explanation', 'Change is measured in relationships, not only symptoms'],
            },
            {
              h: 'What MFT is not',
              body: 'The field is often reduced to “seeing the whole family”. That is a setting, not a theory.',
              items: ['Not the absence of diagnosis', 'Not a denial of biology, trauma or individual experience', 'Not the assumption that families are always the cause'],
            },
            {
              h: 'Why it matters',
              body: 'The unit of treatment decides what counts as data, who is invited in, and what improvement looks like.',
              items: ['Who is present shapes what can be said', 'Relational change can precede symptom change', 'Families are resources, not only risks'],
            },
          ],
          callout: {
            label: 'Working definition', title: 'A discipline of relationship',
            body: 'Marriage and family therapy is the assessment and treatment of relational systems, using theories and methods that treat interaction as the primary site of change.',
          },
          footnote: 'Nichols & Davis (2020); Becvar & Becvar (2018).',
        },
        {
          kind: 'diagram', diagram: 'ecological',
          title: 'The family is nested, not isolated',
          lead: 'A family is never only itself. It is held by kin, community, institutions and policy — each of which can carry a problem or a resource.',
          caption: 'Adapted from Bronfenbrenner’s ecological model; family systems add the dimension of meaning.',
        },
        {
          kind: 'case',
          title: 'The referral that reframes the problem',
          vignette: 'A 14-year-old boy is referred by his school for “defiance and falling grades”. His mother brings him alone. She says, “He is the problem — he won’t listen.” In the first session you learn that his father has worked away for a year, and that the boy now sleeps in his mother’s room.',
          prompts: [
            'What is the presenting problem — and what might it be a solution to?',
            'Who is absent from the room, and what does their absence do?',
            'What would you need to ask before forming a hypothesis?',
          ],
        },
      ],
    },

    // ── WEEK 2 ──────────────────────────────────────────────────────────────
    {
      n: 2, phase: 0,
      title: 'Cybernetics and the Systemic Lens',
      question: 'What kind of explanation does a system require — and what kind of cause is a pattern?',
      outcomes: [
        'Explain negative and positive feedback in family interaction.',
        'Distinguish first-order from second-order cybernetics.',
        'Use punctuation to reframe a presenting complaint.',
      ],
      terms: ['feedback', 'homeostasis', 'circular causality', 'punctuation', 'second-order cybernetics'],
      reading: 'Key reading · Watzlawick, Beavin & Jackson (1967), ch. 1–2 · Bateson (1972), “Cybernetics of self”',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 02',
          title: 'From cause to loop',
          lead: 'Cybernetics gave family therapy its grammar: systems are defined by information fed back into them, not by a single cause acting from outside.',
          blocks: [
            {
              h: 'Feedback',
              body: 'Negative feedback maintains a set point; positive feedback amplifies deviation. Both are orderly — and both can hold a symptom in place.',
              items: ['A thermostat corrects deviation', 'An escalating quarrel amplifies it', 'A symptom can stabilise a system and escalate a conflict'],
            },
            {
              h: 'First and second order',
              body: 'First-order cybernetics assumes an observer outside the system. Second-order cybernetics places the observer inside: the therapist is part of what they describe.',
              items: ['Objectivity in parentheses', 'The therapist’s presence is data', 'Hypotheses are interventions'],
            },
            {
              h: 'Punctuation',
              body: 'Members punctuate the same sequence differently: “I shout because you withdraw” / “I withdraw because you shout”. Both are true; neither is the cause.',
              items: ['Every punctuation implies a culprit', 'Reframing changes the available next move', 'The therapist punctuates too'],
            },
          ],
          callout: {
            label: 'Maturana & Varela', title: 'Objectivity in parentheses',
            body: 'We cannot observe a system without influencing it. The therapist’s presence is part of the system under observation.',
            tone: 'sage',
          },
          footnote: 'Watzlawick, Beavin & Jackson (1967); Bateson (1972).',
        },
        {
          kind: 'diagram', diagram: 'causalLoop',
          title: 'The sequence is the unit of analysis',
          lead: 'A circular map replaces the question “who started it?” with a more useful question: “what keeps it going?”',
          caption: 'Map the loop before attempting to change it.',
        },
        {
          kind: 'seminar',
          title: 'Punctuating a familiar argument',
          lead: 'Work in pairs. Choose an argument you both know well — from your family, your workplace, or the clinic.',
          questions: [
            'Write the argument as a loop with no beginning and no villain.',
            'What does each person’s punctuation protect them from feeling?',
            'Where does “more of the same” appear in the sequence?',
            'What would it mean to intervene at the level of the loop?',
          ],
        },
      ],
    },

    // ── WEEK 3 ──────────────────────────────────────────────────────────────
    {
      n: 3, phase: 0,
      title: 'A Short History of the Field',
      question: 'How did a profession learn to see relationships — and what did it cost to learn?',
      outcomes: [
        'Trace the lineages that produced contemporary MFT.',
        'Explain how the double-bind hypothesis shaped the field.',
        'Situate evidence-based practice within the field’s history.',
      ],
      terms: ['child guidance', 'Palo Alto', 'double bind', 'professionalisation', 'evidence-based practice'],
      reading: 'Key reading · Nichols & Davis (2020), ch. 2–3 · Broderick & Schrader (1991), history of the profession',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 03',
          title: 'Born at the edges of three traditions',
          lead: 'MFT did not begin as a single school. It assembled itself from child guidance, marriage counselling, and a research group studying communication in schizophrenia.',
          blocks: [
            {
              h: '1940s–1950s · separate streams',
              body: 'Child guidance clinics treated the child in context; marriage counselling addressed the couple. Both sat at the margin of a psychiatry organised around the individual.',
            },
            {
              h: '1959 · the double bind',
              body: 'Bateson’s Palo Alto group described contradictory injunctions in families of people diagnosed with schizophrenia. The theory is now read as an early model of relational communication — and a caution about blaming families.',
            },
            {
              h: '1960s–1970s · models proliferate',
              body: 'Structural, strategic, intergenerational, experiential and systemic models emerged, each with its own account of what maintains a problem.',
            },
            {
              h: '1980s–present · profession and evidence',
              body: 'Licensure, accreditation and outcome research — alongside sustained critique from feminist, multicultural and postmodern clinicians.',
            },
          ],
          footnote: 'The “great founders” narrative flattens a field built by many hands — including clients.',
        },
        {
          kind: 'diagram', diagram: 'timeline',
          title: 'Seven moments that made the field',
          lead: 'A selective genealogy, not a complete history: each moment changed what therapists thought they were looking at.',
          caption: 'Dates are approximate and contested; the point is lineage, not chronology.',
        },
        {
          kind: 'case',
          title: 'Reading the present through the past',
          vignette: 'A clinic introduces a manualised parenting programme for every family referred with “behaviour problems”. Clinicians report that families disengage after two sessions. The service manager asks you, as the new MFT, why.',
          prompts: [
            'Which historical tension does this reproduce?',
            'What is lost when a model is applied without systemic assessment?',
            'How would you argue for relational assessment without abandoning evidence?',
          ],
        },
      ],
    },

    // ── WEEK 4 ──────────────────────────────────────────────────────────────
    {
      n: 4, phase: 0,
      title: 'Structural and Strategic Foundations',
      question: 'If the problem lives in the organisation of the family, what exactly do we change?',
      outcomes: [
        'Map boundaries, hierarchy and coalitions in a family.',
        'Distinguish structural from strategic clinical logic.',
        'Design and debrief one enactment.',
      ],
      terms: ['boundary', 'hierarchy', 'subsystem', 'enactment', 'directive'],
      reading: 'Key reading · Minuchin (1974), ch. 1–4 · Haley (1976) · Minuchin & Fishman (1981)',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 04',
          title: 'The architecture of family life',
          lead: 'Structural therapy reads the family as an organised body: who is close to whom, who holds authority, and where the boundaries fall.',
          blocks: [
            {
              h: 'Boundaries',
              body: 'Clear boundaries permit both closeness and separateness. Enmeshed boundaries dissolve autonomy; disengaged boundaries isolate.',
              items: ['Who knows what about whom?', 'Where does a conversation stop being private?', 'Which boundary is too thin, and which too thick?'],
            },
            {
              h: 'Hierarchy and subsystems',
              body: 'Parents need to exercise authority as a subsystem. Children need access to the sibling subsystem — not to the parental one.',
              items: ['Spousal subsystem', 'Parental subsystem', 'Sibling subsystem'],
            },
            {
              h: 'Coalitions',
              body: 'A cross-generational coalition — one parent allied with a child against the other — is a structural signature of many presenting problems.',
              items: ['Who is recruited into which conflict?', 'What does the coalition protect?', 'What would a stronger dyad make possible?'],
            },
          ],
          callout: {
            label: 'Minuchin', title: 'The map is not the family',
            body: 'A structural map is a working hypothesis, drawn to be revised. It is a clinical instrument, not a verdict on the family.',
          },
          footnote: 'Minuchin (1974); Haley (1976).',
        },
        {
          kind: 'diagram', diagram: 'structuralMap',
          title: 'A family, drawn as a system',
          lead: 'Boundaries, hierarchy, coalition and symptom appear in a single view. The genogram is a hypothesis you can test in the room.',
          caption: 'Symbols follow McGoldrick, Gerson & Petry (2008).',
        },
        {
          kind: 'case',
          title: 'A family that cannot agree on the problem',
          vignette: 'A mother complains that her husband “undermines” her with their 15-year-old daughter. The father says the mother is “too strict”. The daughter says nothing. When the parents begin to argue, the daughter interrupts with a headache and the argument stops.',
          prompts: [
            'Draw the subsystem boundaries and the triangle.',
            'What is the daughter’s headache doing in the system?',
            'Which dyad would you strengthen first — and why?',
          ],
        },
      ],
    },

    // ── WEEK 5 ──────────────────────────────────────────────────────────────
    {
      n: 5, phase: 1,
      title: 'Intergenerational and Contextual Approaches',
      question: 'How does the past continue to speak in the present — and who is loyal to whom?',
      outcomes: [
        'Explain differentiation of self and triangulation.',
        'Construct and interpret a three-generation genogram.',
        'Apply the concepts of legacy, entitlement and loyalty.',
      ],
      terms: ['differentiation', 'triangle', 'multigenerational transmission', 'legacy', 'loyalty'],
      reading: 'Key reading · Bowen (1978), ch. 1–3 · Kerr & Bowen (1988) · Boszormenyi-Nagy & Spark (1973)',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 05',
          title: 'The emotional process that travels',
          lead: 'Bowen shifted attention from the presenting symptom to the emotional process that moves through generations — and to the therapist’s own family as an instrument of understanding.',
          blocks: [
            {
              h: 'Differentiation of self',
              body: 'The capacity to stay connected while maintaining one’s own thinking. Low differentiation produces fusion, reactivity and the feeling that one cannot survive the other’s disapproval.',
              items: ['Thinking versus feeling', 'Solid self versus pseudo-self', 'The goal is connection, not distance'],
            },
            {
              h: 'Triangles',
              body: 'Under tension, dyads recruit a third. Triangles distribute anxiety — and freeze conflict in place.',
              items: ['Who is recruited when tension rises?', 'Which side carries the symptom?', 'Can each dyad be strengthened without the third?'],
            },
            {
              h: 'Legacy and loyalty',
              body: 'Boszormenyi-Nagy added an ethical dimension: families keep a ledger of give-and-take. Entitlement, loyalty and invisible debts shape what members feel they owe.',
              items: ['What was handed down that was not chosen?', 'What loyalty would change require?', 'Where is fairness being negotiated?'],
            },
          ],
          callout: {
            label: 'A caution', title: 'Explaining is not excusing',
            body: 'Intergenerational work describes transmission. It does not absolve responsibility, and it must never be used to blame a previous generation for a present choice.',
          },
          footnote: 'Bowen (1978); Kerr & Bowen (1988); Boszormenyi-Nagy & Spark (1973).',
        },
        {
          kind: 'diagram', diagram: 'triangle',
          title: 'The triangle as the unit of emotional process',
          lead: 'Bowen’s smallest stable relational system is not the dyad but the triangle. Anxiety moves; the third person absorbs it.',
          caption: 'After Bowen (1978); see also Kerr & Bowen (1988).',
        },
        {
          kind: 'seminar',
          title: 'The ledger of loyalty',
          lead: 'This is a reflective seminar. Speak only to what you are willing to share; the exercise is about seeing, not disclosing.',
          questions: [
            'What was handed down to you that you did not choose?',
            'What loyalty would be tested if you changed one pattern?',
            'Where does “undifferentiated” appear in your own family?',
            'How would you ask about legacy without pathologising it?',
          ],
        },
      ],
    },

    // ── WEEK 6 ──────────────────────────────────────────────────────────────
    {
      n: 6, phase: 1,
      title: 'Experiential and Humanistic Traditions',
      question: 'What happens when the therapist stops explaining and starts experiencing?',
      outcomes: [
        'Describe Satir’s communication stances and the goal of congruence.',
        'Explain the symbolic-experiential use of the therapist’s self.',
        'Practise immediacy without shaming.',
      ],
      terms: ['congruence', 'sculpting', 'immediacy', 'symbolic-experiential', 'self-of-the-therapist'],
      reading: 'Key reading · Satir (1967) · Whitaker (1989) · Greenberg & Johnson (1988)',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 06',
          title: 'The person of the therapist',
          lead: 'Experiential models insist that change happens in the encounter — not in the explanation of the encounter.',
          blocks: [
            {
              h: 'Satir · communication and congruence',
              body: 'Stances are survival strategies learned early: placating, blaming, being super-reasonable, being irrelevant. Congruence is the goal — the body, the words and the feeling agreeing.',
              items: ['Sculpting makes structure visible in space', 'The therapist models congruence rather than teaching it', 'Family maps trace three generations of coping'],
            },
            {
              h: 'Whitaker · symbolic-experiential',
              body: 'Therapy trusts the family’s own process. The therapist joins, provokes, plays and uses their own experience as part of the field.',
              items: ['The therapist’s growth is part of the treatment', 'Symptoms can be understood symbolically', 'Play is a serious clinical method'],
            },
            {
              h: 'The emotion-focused lineage',
              body: 'Greenberg and Johnson moved experiential work toward affect regulation and attachment, making it researchable without losing its human centre.',
              items: ['Emotion as information', 'Therapeutic presence', 'A bridge to process research'],
            },
          ],
          callout: {
            label: 'Whitaker', title: 'The self as instrument',
            body: 'Personal therapy and supervision are not extras added to training. They are the means by which the therapist becomes usable.',
            tone: 'sage',
          },
          footnote: 'Satir (1967); Whitaker (1989); Greenberg & Johnson (1988).',
        },
        {
          kind: 'diagram', diagram: 'stances',
          title: 'Four stances, one cost each',
          lead: 'Each stance solves an immediate problem and purchases a longer one. The clinical task is to make the cost visible without contempt.',
          caption: 'After Virginia Satir’s communication stances.',
        },
        {
          kind: 'case',
          title: 'The family that explains everything',
          vignette: 'A couple arrives with a spreadsheet of grievances. Each has rehearsed their account. When you ask what each felt during the argument, both answer with the other’s motives. The session is calm, articulate, and completely stuck.',
          prompts: [
            'What is the function of the explanation?',
            'How would you move from story to affect without shaming?',
            'What would immediacy look like here?',
          ],
        },
      ],
    },

    // ── WEEK 7 ──────────────────────────────────────────────────────────────
    {
      n: 7, phase: 1,
      title: 'Postmodern and Constructivist Turns',
      question: 'If meaning is made in language, what is therapy making?',
      outcomes: [
        'Compare first-order systemic and postmodern practice.',
        'Describe solution-focused and narrative methods.',
        'Use an externalising question in a role-play.',
      ],
      terms: ['social constructionism', 'externalising', 'exception', 'not-knowing', 'reflecting team'],
      reading: 'Key reading · White & Epston (1990), ch. 2–4 · de Shazer (1985) · Andersen (1991)',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 07',
          title: 'Meaning as the material of therapy',
          lead: 'Postmodern practice shifted the therapist’s authority from diagnosis to curiosity — and made the family’s language the central clinical material.',
          blocks: [
            {
              h: 'Milan systemic',
              body: 'Hypothesising, circularity and neutrality: the team’s ideas are provisional, and difference is the engine of change.',
              items: ['Hypotheses are held, not owned', 'Circular questions reveal difference', 'Neutrality is curiosity in action'],
            },
            {
              h: 'Solution-focused',
              body: 'Problems have exceptions; change is already occurring. The miracle question, scaling and exception-finding orient the family toward what already works.',
              items: ['Assume competence', 'Amplify exceptions', 'Small change is enough to begin'],
            },
            {
              h: 'Narrative',
              body: 'Problems are stories, not essences. Externalising separates the person from the problem; unique outcomes open a preferred story.',
              items: ['“The anxiety visits you” rather than “you are anxious”', 'Deconstruct the dominant story', 'Re-author in the family’s own language'],
            },
          ],
          callout: {
            label: 'Critique', title: 'Not-knowing is not ignorance',
            body: 'The therapist remains accountable for power, ethics and outcome. Curiosity does not suspend responsibility for safety.',
            tone: 'sage',
          },
          footnote: 'Selvini Palazzoli et al. (1978); de Shazer (1985); White & Epston (1990); Andersen (1991).',
        },
        {
          kind: 'diagram', diagram: 'matrix',
          title: 'Two epistemologies, held side by side',
          lead: 'The distinction is not a war. Most contemporary practitioners move between these positions within a single session.',
          caption: 'After Cecchin (1987) and White & Epston (1990).',
        },
        {
          kind: 'case',
          title: 'Externalising a diagnosis',
          vignette: 'Parents describe their 10-year-old as “the ADHD child”. School reports dominate dinner-table conversation. The boy says, “I’m the naughty one.”',
          prompts: [
            'What might it mean to externalise ADHD without dismissing it?',
            'What unique outcomes exist in the family’s own account?',
            'Where does the family’s preferred story begin?',
          ],
        },
      ],
    },

    // ── WEEK 8 ──────────────────────────────────────────────────────────────
    {
      n: 8, phase: 1,
      title: 'Integrative Case Conceptualisation',
      question: 'How does a therapist choose a theory — and then hold it lightly?',
      outcomes: [
        'Compare formulations of one family across four models.',
        'Write a systemic formulation that includes risk and context.',
        'Defend a reasoned choice of intervention.',
      ],
      terms: ['formulation', 'hypothesis', 'maintaining pattern', 'integration'],
      reading: 'Key reading · Carr (2019), ch. 4 · Eells (2015), case formulation',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 08',
          title: 'Formulation as a disciplined hypothesis',
          lead: 'A formulation is not a diagnosis with a story attached. It is a testable account of how a problem is maintained, in this system, at this moment.',
          blocks: [
            {
              h: 'What a formulation must do',
              body: 'Explain the presenting problem, identify maintaining patterns, locate strengths, specify a point of leverage, and anticipate risk.',
              items: ['Description before explanation', 'Maintaining patterns, not only origins', 'A plan that can be revised'],
            },
            {
              h: 'Four Ps, systemically',
              body: 'Predisposing, precipitating, perpetuating and protective factors — each located in the family’s relational and social context.',
              items: ['Predisposing · history and temperament', 'Precipitating · events and transitions', 'Perpetuating · cycles, coalitions, meanings'],
            },
            {
              h: 'Holding theory lightly',
              body: 'Different models illuminate different surfaces. The question is not which model is true, but which formulation opens the most useful next step.',
              items: ['Use more than one lens', 'Let the family’s feedback correct you', 'Integration is a discipline, not a blend'],
            },
          ],
          callout: {
            label: 'Assessment', title: 'Formative case formulation',
            body: 'Due in Week 9. One family, three formulations and a defended intervention plan, 2,500 words.',
          },
          footnote: 'Carr (2019); Eells (2015).',
        },
        {
          kind: 'diagram', diagram: 'formulation',
          title: 'One family, four formulations',
          lead: 'The same presenting problem yields four different accounts of what maintains it — and four different first moves.',
          caption: 'A comparative grid for the Week 9 written formulation.',
        },
        {
          kind: 'seminar',
          title: 'Same family, four lenses',
          lead: 'Using the family from your case formulation, argue the case for each model in turn — then choose one and justify the choice.',
          questions: [
            'What does each model see that the others miss?',
            'Where do the formulations contradict one another?',
            'Which intervention follows from your chosen account?',
            'What would count as evidence that you were wrong?',
          ],
        },
      ],
    },

    // ── WEEK 9 ──────────────────────────────────────────────────────────────
    {
      n: 9, phase: 2,
      title: 'The First Session and the Therapeutic Alliance',
      question: 'How do you join a system without joining its triangles?',
      outcomes: [
        'Structure a first session from opening to next steps.',
        'Build and monitor a multi-person alliance.',
        'Negotiate consent and confidentiality with several clients.',
      ],
      terms: ['joining', 'alliance', 'neutrality', 'informed consent', 'split alliance'],
      reading: 'Key reading · Minuchin & Fishman (1981), ch. 1–2 · Friedlander, Escudero & Heatherington (2006)',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 09',
          title: 'Joining before intervening',
          lead: 'The first session is already an intervention. It establishes who is heard, what is named as the problem, and whether change feels possible.',
          blocks: [
            {
              h: 'The tasks of session one',
              body: 'Engage every member, establish safety and consent, elicit each description, observe sequences, offer a tentative formulation, agree next steps.',
              items: ['Who speaks first — and who is spoken for?', 'What is the family’s own explanation?', 'What has already been tried?'],
            },
            {
              h: 'The multi-person alliance',
              body: 'In couple and family work the alliance is not one relationship but several — and they can conflict.',
              items: ['Bond, goals, tasks', 'Split alliances reproduce triangles', 'Rupture is data, not failure'],
            },
            {
              h: 'Neutrality, revised',
              body: 'Neutrality is not indifference. It is a commitment not to become the spokesperson for any one member — including the most articulate one.',
              items: ['Curiosity over alignment', 'Multidirectional partiality', 'The absent member is still in the room'],
            },
          ],
          callout: {
            label: 'Consent', title: 'Who is the client?',
            body: 'With multiple clients, consent must specify who holds confidentiality, how records are shared, and what happens when members disagree about disclosure.',
          },
          footnote: 'Minuchin & Fishman (1981); Pinsof & Wynne (1995).',
        },
        {
          kind: 'diagram', diagram: 'alliance',
          title: 'The alliance is not a dyad',
          lead: 'Every statement is heard by more than one person — and heard differently. The therapist’s task is to remain available to all of them.',
          caption: 'After Friedlander, Escudero & Heatherington (2006).',
        },
        {
          kind: 'case',
          title: 'The first ten minutes',
          vignette: 'A couple arrives furious. One wants to leave; the other booked the session secretly. Both look at you before they sit down.',
          prompts: [
            'What do you say in the first minute?',
            'How do you handle the secret booking?',
            'What would make both feel heard without agreeing with either?',
          ],
        },
      ],
    },

    // ── WEEK 10 ─────────────────────────────────────────────────────────────
    {
      n: 10, phase: 2,
      title: 'Assessment, Genograms and Information Gathering',
      question: 'What must a therapist know before intervening — and what does the asking itself do?',
      outcomes: [
        'Construct a three-generation genogram with a family.',
        'Use circular questions to elicit relational difference.',
        'Integrate risk screening into systemic assessment.',
      ],
      terms: ['genogram', 'circular questioning', 'interventive interviewing', 'risk assessment'],
      reading: 'Key reading · McGoldrick, Gerson & Petry (2008), ch. 1–3 · Tomm (1988), interventive interviewing',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 10',
          title: 'Assessment as a relational act',
          lead: 'Every question is an intervention: it directs attention, invites a description, and positions the family in relation to the problem.',
          blocks: [
            {
              h: 'The genogram',
              body: 'Three generations, drawn with the family, in the first two sessions. The drawing matters less than the conversation it makes possible.',
              items: ['Structure · household, marriages, births, deaths, migration', 'Patterns · repetition, cut-offs, coalitions', 'Meaning · names, legacies, secrets'],
            },
            {
              h: 'Circular questioning',
              body: 'Questions about difference and connection: “Who is most worried? Who shows it least? What does your mother do when your father goes quiet?”',
              items: ['Ask about relationships, not individuals', 'Ask each member to compare', 'Let the question land before asking the next'],
            },
            {
              h: 'Risk and safeguarding',
              body: 'Ask directly, document clearly, consult, and follow local law and agency procedure. Risk assessment is not a form; it is a conversation with consequences.',
              items: ['Violence and coercive control', 'Self-harm and suicidal ideation', 'Child protection and elder safety'],
            },
          ],
          callout: {
            label: 'Tomm', title: 'Questions have effects',
            body: 'Interventive interviewing treats the question as a clinical move: it creates difference, opens possibility, or closes a conversation.',
            tone: 'sage',
          },
          footnote: 'McGoldrick, Gerson & Petry (2008); Tomm (1988); Fleuridas, Nelson & Rosenthal (1986).',
        },
        {
          kind: 'diagram', diagram: 'genogram',
          title: 'Three generations in one view',
          lead: 'A genogram turns history into a hypothesis: where the family repeats, where it cuts off, and where the symptom sits.',
          caption: 'Conventions after McGoldrick, Gerson & Petry (2008).',
        },
        {
          kind: 'case',
          title: 'The family who would not draw',
          vignette: 'The parents decline the genogram: “We don’t talk about the past.” The 17-year-old asks whether their uncle is “the one nobody mentions”.',
          prompts: [
            'What is the refusal protecting?',
            'How do you honour the boundary and stay curious?',
            'What does the adolescent already know — and what is that knowledge doing?',
          ],
        },
      ],
    },

    // ── WEEK 11 ─────────────────────────────────────────────────────────────
    {
      n: 11, phase: 2,
      title: 'Ethics, Law and Professional Governance',
      question: 'Whose confidence is it, when the client is a family?',
      outcomes: [
        'Apply the AAMFT Code of Ethics to multi-client dilemmas.',
        'Manage confidentiality, secrets and record-sharing.',
        'Document ethical decisions defensibly.',
      ],
      terms: ['informed consent', 'confidentiality', 'duty to warn', 'competence', 'documentation'],
      reading: 'Key reading · AAMFT (2015), Code of Ethics · Corey, Corey & Callanan (2019), ch. 6–8',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 11',
          title: 'The ethical complexity of the many',
          lead: 'Family therapy multiplies the number of people to whom the therapist owes a duty — and the number of ways those duties can collide.',
          blocks: [
            {
              h: 'Consent is continuous',
              body: 'Consent is not a signature at intake. It is a conversation renewed whenever the system changes — a new partner, an adolescent, a court order.',
              items: ['Who is the client?', 'What has each member agreed to?', 'What changes when someone joins or leaves?'],
            },
            {
              h: 'Confidentiality is not singular',
              body: 'Who owns the record? Who may see it? What happens to a secret disclosed by one member? These questions must be answered before they are urgent.',
              items: ['Secrets within the system', 'Records and third parties', 'Limits required by law'],
            },
            {
              h: 'Boundaries and competence',
              body: 'Multiple relationships are endemic in small communities. Competence is an ethical obligation, not a personal achievement.',
              items: ['Recognise the limits of your training', 'Seek supervision early', 'Document the reasoning, not only the outcome'],
            },
          ],
          callout: {
            label: 'AAMFT Code', title: 'Nonmaleficence first',
            body: 'When duties conflict, the standard is the least harm and the most transparency achievable. Consultation is both a safeguard and an ethical practice.',
          },
          footnote: 'AAMFT (2015); Corey, Corey & Callanan (2019).',
        },
        {
          kind: 'diagram', diagram: 'ethicsTree',
          title: 'Deciding what may be shared',
          lead: 'A decision pathway for the most common ethical pressure in family work: the secret in the room.',
          caption: 'Adapt to your jurisdiction, agency policy and professional code.',
        },
        {
          kind: 'seminar',
          title: 'The secret in the room',
          lead: 'A mother tells you, alone, that she is planning to leave her husband. She asks you not to tell him. The couple is due in twenty minutes.',
          questions: [
            'What did you promise at intake — explicitly and implicitly?',
            'What are the risks of holding the secret, and of disclosing it?',
            'What would you say, and to whom, in the next session?',
            'How would you document your reasoning?',
          ],
        },
      ],
    },

    // ── WEEK 12 ─────────────────────────────────────────────────────────────
    {
      n: 12, phase: 2,
      title: 'Culture, Power and Social Location',
      question: 'Whose normal is the therapy measuring against?',
      outcomes: [
        'Apply cultural humility as a clinical stance.',
        'Use the ADDRESSING framework to map social location.',
        'Interrogate your own cultural assumptions in supervision.',
      ],
      terms: ['cultural humility', 'intersectionality', 'power', 'cultural genogram', 'positionality'],
      reading: 'Key reading · Hays (2016), ch. 1–4 · McGoldrick, Giordano & Garcia-Preto (2005)',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 12',
          title: 'Culture is not a variable; it is the water',
          lead: 'Every family is cultural, including the therapist’s. The question is not whether culture matters, but whose cultural assumptions are doing the work.',
          blocks: [
            {
              h: 'Beyond competence',
              body: 'Cultural competence risks treating culture as a checklist. Cultural humility is a stance: self-reflection, attention to power, and lifelong learning.',
              items: ['Notice your own location', 'Treat the family as expert on its culture', 'Expect to be corrected'],
            },
            {
              h: 'Intersectionality and power',
              body: 'Race, class, gender, faith, migration status and sexuality intersect. No single identity explains a family — and the therapist’s institution is part of the power in the room.',
              items: ['Who is speaking, and who is spoken about?', 'Who is absent?', 'What does the family have to risk to be understood?'],
            },
            {
              h: 'Local context',
              body: 'In Nigeria and across Africa, extended kin, faith communities and communal child-rearing are central resources — and sometimes sites of obligation, surveillance and conflict.',
              items: ['Kinship as support and constraint', 'Faith as coping and as authority', 'Migration and the transnational family'],
            },
          ],
          callout: {
            label: 'Hardy & Laszloffy (1995)', title: 'The cultural genogram',
            body: 'Map the family’s cultural identity, migration, language and the meanings attached to difference — including what the family was taught to think about other groups.',
            tone: 'sage',
          },
          footnote: 'Hays (2016); Falicov (2014); Hardy & Laszloffy (1995).',
        },
        {
          kind: 'diagram', diagram: 'addressing',
          title: 'Mapping social location',
          lead: 'ADDRESSING asks the therapist to locate themselves before locating the family — and to notice which differences carry power in this room.',
          caption: 'Framework after Hays (2016).',
        },
        {
          kind: 'case',
          title: 'The interpreter in the room',
          vignette: 'A family recently arrived from a rural area speaks a language you do not share. The interpreter is a member of their faith community. The parents defer to the interpreter; the daughter answers in the dominant language.',
          prompts: [
            'What are the risks of using a community interpreter?',
            'How do you protect the daughter’s voice?',
            'What would you need to ask about the family’s own explanation?',
          ],
        },
      ],
    },

    // ── WEEK 13 ─────────────────────────────────────────────────────────────
    {
      n: 13, phase: 3,
      title: 'Children, Adolescents and Parenting',
      question: 'How does a child’s symptom speak for the family — and to it?',
      outcomes: [
        'Conduct child-inclusive family sessions.',
        'Apply a developmental frame to presenting problems.',
        'Work with the parental subsystem as a coalition.',
      ],
      terms: ['parentification', 'developmental task', 'triangulation', 'parenting coalition'],
      reading: 'Key reading · Combrinck-Graham (2006) · Sori & Hecker (2015)',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 13',
          title: 'The child in the system',
          lead: 'Children are often the reason a family comes — and the least powerful person in the room.',
          blocks: [
            {
              h: 'Development as constraint',
              body: 'What looks like defiance at 14 may be a developmentally ordinary bid for autonomy; what looks like independence at 7 may be neglect.',
              items: ['Development is relational, not only biological', 'Behaviour is age-referenced', 'The symptom may be on schedule'],
            },
            {
              h: 'Triangulation and parentification',
              body: 'A child recruited into parental conflict may present the symptom. A child who cares for a parent may present competence — and neither is a diagnosis.',
              items: ['Who is protecting whom?', 'Who has been promoted to adult?', 'What does the child’s behaviour hold together?'],
            },
            {
              h: 'Parenting as a subsystem',
              body: 'Effective parenting requires a coalition between caregivers, not a coalition with the child. Agreement is not uniformity.',
              items: ['Negotiate the frame before the rules', 'Support the weaker parental voice', 'Keep children out of the executive'],
            },
          ],
          callout: {
            label: 'Alliance', title: 'The adolescent’s confidence',
            body: 'Adolescents need a space that is theirs. Confidentiality must be negotiated explicitly with parents — and its limits stated in advance.',
          },
          footnote: 'Combrinck-Graham (2006); Sori & Hecker (2015).',
        },
        {
          kind: 'diagram', diagram: 'devTimeline',
          title: 'Development as a clinical frame',
          lead: 'Each stage carries a task, a vulnerability and a particular way of speaking without words.',
          caption: 'Read alongside the family life cycle (Week 15).',
        },
        {
          kind: 'case',
          title: 'The symptomatic child',
          vignette: 'A 9-year-old refuses school. Her parents disagree about whether she is “manipulative” or “anxious”. Her mother has recently returned to full-time work; her father works nights.',
          prompts: [
            'What developmental and family transitions converge here?',
            'What is the school refusal doing for the system?',
            'Who needs to be in the next session?',
          ],
        },
      ],
    },

    // ── WEEK 14 ─────────────────────────────────────────────────────────────
    {
      n: 14, phase: 3,
      title: 'Couple Relationships, Attachment and Repair',
      question: 'What if the problem is not the argument, but the cycle beneath it?',
      outcomes: [
        'Describe attachment cycles in couple distress.',
        'Map a pursuer–withdrawer sequence.',
        'Identify and rehearse a repair move.',
      ],
      terms: ['negative cycle', 'attachment', 'pursuer–withdrawer', 'repair'],
      reading: 'Key reading · Johnson (2019), ch. 1–4 · Gottman & Gottman (2017)',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 14',
          title: 'The cycle beneath the argument',
          lead: 'Couples do not fight about the dishes. They fight about whether they matter to each other — and the dishes are the only vocabulary available.',
          blocks: [
            {
              h: 'Attachment in adulthood',
              body: 'Proximity-seeking, safe haven, secure base: the needs that organise infancy organise marriage. Attachment is not dependency; it is how humans regulate fear.',
              items: ['Protest behaviours signal threat', 'Withdrawal protects and abandons', 'Security is built in small repetitions'],
            },
            {
              h: 'The pursuer–withdrawer cycle',
              body: 'Protest and withdrawal are two versions of the same attachment cry. Each triggers the other, and each is experienced as the cause.',
              items: ['Criticism invites distance', 'Distance confirms abandonment', 'The cycle, not the partner, is the problem'],
            },
            {
              h: 'Repair',
              body: 'Repair is not the absence of conflict. It is the return to connection after rupture — and it can be learned.',
              items: ['Name the cycle', 'Validate the fear beneath the move', 'Risk a new response'],
            },
          ],
          callout: {
            label: 'Emotionally focused therapy', title: 'Change the cycle, not the person',
            body: 'EFT tracks the cycle, accesses the attachment emotion, and stages a new conversation in which each partner can be reached.',
            tone: 'sage',
          },
          footnote: 'Johnson (2019); Gottman & Gottman (2017); Epstein & Baucom (2002).',
        },
        {
          kind: 'diagram', diagram: 'cycle',
          title: 'Mapping the negative cycle',
          lead: 'A three-move loop, repeated thousands of times, until it feels like the truth about the relationship.',
          caption: 'After Johnson (2019).',
        },
        {
          kind: 'seminar',
          title: 'The argument underneath',
          lead: 'In pairs, take one repeated argument and map it as an attachment cycle rather than a disagreement.',
          questions: [
            'What is each partner asking for beneath the complaint?',
            'Which move most reliably triggers the other?',
            'Where could a softer signal be risked?',
            'What would make repair credible rather than polite?',
          ],
        },
      ],
    },

    // ── WEEK 15 ─────────────────────────────────────────────────────────────
    {
      n: 15, phase: 3,
      title: 'Family Transitions, Crisis and High-Conflict Contexts',
      question: 'When the family changes shape, what holds it together — and what must be made safe first?',
      outcomes: [
        'Map transitions using a family life cycle frame.',
        'Assess safety and crisis in family work.',
        'Work systemically with separation and stepfamily formation.',
      ],
      terms: ['transition', 'family life cycle', 'ambiguous loss', 'coercive control', 'safety plan'],
      reading: 'Key reading · Carter & McGoldrick (1999), ch. 1–2 · Walsh (2016) · Emery (2012)',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 15',
          title: 'Symptoms at the threshold',
          lead: 'Families do not present at random. Symptoms cluster at transitions — when the old rules no longer fit and the new ones do not yet exist.',
          blocks: [
            {
              h: 'The family life cycle',
              body: 'Stages and transitions; vertical stressors (history, legacy) meet horizontal stressors (events, time). The symptom often appears in the in-between.',
              items: ['Not a timetable but a set of tasks', 'Transitions renegotiate every relationship', 'Cultural timing varies widely'],
            },
            {
              h: 'Crisis and safety',
              body: 'Crisis compresses time. The first tasks are safety and stabilisation; meaning-making comes after the system can hold it.',
              items: ['Screen for violence separately', 'Do not do couple work under coercive control', 'Document and refer'],
            },
            {
              h: 'Separation and stepfamily',
              body: 'Divorce is not an event but a process. Co-parenting requires a new boundary around the couple relationship — and stepfamily formation requires time.',
              items: ['Grief alongside relief', 'Loyalty conflicts', 'A slower integration than adults expect'],
            },
          ],
          callout: {
            label: 'Ambiguous loss', title: 'Present and absent at once',
            body: 'When a person is physically absent but psychologically present — or the reverse — grief cannot close. Naming the ambiguity can restore movement.',
            tone: 'sage',
          },
          footnote: 'Carter & McGoldrick (1999); Walsh (2016); Emery (2012).',
        },
        {
          kind: 'diagram', diagram: 'lifeCycle',
          title: 'The staircase of transitions',
          lead: 'Each step up requires the family to reorganise. The step down is where symptoms often appear.',
          caption: 'After Carter & McGoldrick (1999).',
        },
        {
          kind: 'case',
          title: 'The transition nobody named',
          vignette: 'A family seeks help because their 16-year-old has “become impossible”. The eldest child left for university last term; the grandmother moved in after a stroke three months ago.',
          prompts: [
            'Which transitions are stacking up?',
            'What meaning does the adolescent’s behaviour carry?',
            'What would stabilisation look like in the first three sessions?',
          ],
        },
      ],
    },

    // ── WEEK 16 ─────────────────────────────────────────────────────────────
    {
      n: 16, phase: 3,
      title: 'Evidence, Outcomes and Professional Identity',
      question: 'How will you know your work is helping — and who are you becoming as a therapist?',
      outcomes: [
        'Explain common factors and evidence-based practice.',
        'Use routine outcome monitoring in a session.',
        'Write a professional development and supervision plan.',
      ],
      terms: ['common factors', 'evidence-based practice', 'routine outcome monitoring', 'reflective practice'],
      reading: 'Key reading · Sprenkle, Davis & Lebow (2009) · Wampold & Imel (2015) · Duncan et al. (2010)',
      slides: [
        {
          kind: 'concept', kicker: 'Lecture 16',
          title: 'What makes therapy work',
          lead: 'Models differ; the factors that carry change overlap. Evidence is not the enemy of relationship — it is a discipline of humility.',
          blocks: [
            {
              h: 'Common factors',
              body: 'Alliance, empathy, expectancy and client resources account for substantial variance across models — which is why the therapeutic relationship is a clinical variable, not a pleasant extra.',
              items: ['Alliance as outcome predictor', 'Therapist effects are real', 'Fit the model to the family'],
            },
            {
              h: 'Evidence-based practice',
              body: 'EBP is the integration of best research, clinical expertise and client values — not the mechanical application of a manual.',
              items: ['Know the evidence base for your model', 'Adapt without abandoning fidelity', 'Name uncertainty honestly'],
            },
            {
              h: 'Routine outcome monitoring',
              body: 'Measure each session; review with the client; act early on deterioration. Feedback turns the client’s view into clinical data.',
              items: ['ORS and SRS', 'Review the score together', 'Escalate, consult, or change method'],
            },
          ],
          callout: {
            label: 'Feedback-informed', title: 'The client’s view',
            body: 'The most predictive feedback is not the therapist’s evaluation of the session, but the client’s experience of alliance and outcome.',
          },
          footnote: 'Sprenkle, Davis & Lebow (2009); Wampold & Imel (2015); Duncan et al. (2010).',
        },
        {
          kind: 'diagram', diagram: 'outcomes',
          title: 'Feedback as a clinical discipline',
          lead: 'Measurement is not surveillance. Done well, it is a structured conversation about whether this work is helping this family.',
          caption: 'ORS — Outcome Rating Scale; SRS — Session Rating Scale.',
        },
        {
          kind: 'seminar',
          title: 'The clinician you are becoming',
          lead: 'A closing seminar. Speak from your own experience; listen without advising.',
          questions: [
            'Which model feels most like you — and what does that reveal?',
            'Where are you most likely to lose your curiosity?',
            'What would you want a supervisor to notice about you?',
            'What is one commitment you will carry into practicum?',
          ],
        },
      ],
    },
  ],

  glossary: [
    ['Circular causality', 'A sequence in which each response becomes the stimulus for the next.'],
    ['Punctuation', 'The arbitrary point at which a member says a circular sequence begins.'],
    ['Homeostasis', 'The system’s tendency to maintain a familiar set point.'],
    ['Feedback', 'Information about the effect of an action that modifies subsequent action.'],
    ['Boundary', 'The invisible rule regulating closeness and distance between subsystems.'],
    ['Triangulation', 'Recruiting a third person to manage tension between two.'],
    ['Differentiation of self', 'Staying connected while maintaining one’s own thinking.'],
    ['Enactment', 'Inviting the family to re-enact a problematic interaction in session.'],
    ['Genogram', 'A multigenerational diagram of structure, relationships and patterns.'],
    ['Joining', 'The therapist’s active accommodation to the family’s style and language.'],
    ['Alliance', 'The collaborative bond and agreement on goals and tasks.'],
    ['Externalising', 'Treating the problem as separate from the person.'],
    ['Circular questioning', 'Questions that elicit differences and connections within the system.'],
    ['Neutrality', 'A commitment not to align with any one member’s account.'],
    ['Cultural humility', 'A reflexive, lifelong stance toward one’s own cultural location.'],
    ['Common factors', 'Change processes shared across therapeutic models.'],
    ['Reflecting team', 'A team whose conversation is observed by the family.'],
    ['Self-of-the-therapist', 'The clinician’s own relational history and reactivity as clinical material.'],
  ],

  references: [
    'AAMFT (2015). Code of Ethics. American Association for Marriage and Family Therapy.',
    'Bateson, G. (1972). Steps to an Ecology of Mind. Chandler.',
    'Becvar, R. J., & Becvar, D. S. (2018). Systems Theory and Family Therapy: A Primer (3rd ed.). Hamilton.',
    'Bowen, M. (1978). Family Therapy in Clinical Practice. Jason Aronson.',
    'Carr, A. (2019). Family Therapy: Concepts, Process and Practice (3rd ed.). Wiley.',
    'de Shazer, S. (1985). Keys to Solution in Brief Therapy. Norton.',
    'Duncan, B. L., Miller, S. D., Wampold, B. E., & Hubble, M. A. (Eds.). (2010). The Heart and Soul of Change (2nd ed.). APA.',
    'Haley, J. (1976). Problem-Solving Therapy. Jossey-Bass.',
    'Johnson, S. M. (2019). Attachment Theory in Practice. Guilford.',
    'McGoldrick, M., Gerson, R., & Petry, S. (2008). Genograms: Assessment and Intervention (3rd ed.). Norton.',
    'Minuchin, S. (1974). Families and Family Therapy. Harvard University Press.',
    'Nichols, M. P., & Davis, S. D. (2020). Family Therapy: Concepts and Methods (12th ed.). Pearson.',
    'Satir, V. (1967). Conjoint Family Therapy. Science and Behavior Books.',
    'Watzlawick, P., Beavin, J. H., & Jackson, D. D. (1967). Pragmatics of Human Communication. Norton.',
    'White, M., & Epston, D. (1990). Narrative Means to Therapeutic Ends. Norton.',
    'Wampold, B. E., & Imel, Z. E. (2015). The Great Psychotherapy Debate (2nd ed.). Routledge.',
  ],

  closing: {
    title: 'The family is not the context of the problem.',
    body: 'It is the context of the solution — and the place where a therapist learns to be useful.',
    next: 'Next in the programme · MFT 702 — Theories of Family Therapy',
  },
};

export default course;
