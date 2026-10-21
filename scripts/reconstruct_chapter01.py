"""Apply approved, source-supported Chapter 1 additions; no invented references."""
from pathlib import Path
import re,json
p=Path('manuscript/chapter01.md')
s=Path('editorial/archive/chapter01-proof01.md').read_text()
s=s.replace('**Developmental proof 01 · Not approved for publication**','**Scholarly reconstruction proof 02 · Not approved for publication**')
a=s.index('This proof reconstructs');b=s.index('## Learning objectives')
s=s[:a]+'This doctoral-level proof incorporates the author-approved reconstruction of missing material. Source-based additions are cited and documented in the accompanying evidence register. The wider book remains under editorial review; this is not a released edition.\n\n'+s[b:]
s=s.replace('Historical discussion is limited to the broad methodological progression documented in the supplied text; it should not be read as a complete history of the field.','The historical discussion explains how research questions changed as investigators moved from regulation and lesion observations to physiological measurement, endocrine assays, and imaging. These developments should be evaluated through their methods and limits rather than treated as a simple accumulation of increasingly definitive tests.')
s=s.replace('Terms require clear boundaries. A mechanism, a measurement, and an outcome may be related without being interchangeable. The supplied text repeatedly names homeostasis, allostasis, adaptation, and biomarkers, but several of its definition passages do not actually define the named term. Those passages have not been reproduced as valid definitions; their completion is recorded as an author query.', '''### 1.2.3 Foundational distinctions

**Homeostasis** concerns regulation that maintains physiological variables within viable ranges. Stability is actively maintained; it does not mean that a living system is static. **Allostasis** emphasises adjustments in regulation as conditions and demands change. These concepts overlap, and the usefulness of treating them as distinct explanatory frameworks has been debated (Goldstein & Kopin, 2007; Godoy et al., 2018).

**Adaptation**, in this discussion, denotes physiological or behavioural adjustments through which an organism responds to changing demands. An adjustment that is useful in one setting need not remain useful under persistent or different demands. **Allostatic load** concerns the cumulative burden associated with sustained or repeated regulatory demands; it should not be used as an interchangeable label for a stressful event, a symptom score, or a diagnosis (Goldstein & Kopin, 2007; Godoy et al., 2018).

A **biomarker** is a measured characteristic used to indicate a biological process or a biological response to an exposure or intervention. Biomarkers can be molecular, histological, imaging-based, or physiological. Their intended use must be specified. A biomarker is not the same as a measure of how a person feels or functions, and a measured association alone does not establish diagnostic usefulness (U.S. Food and Drug Administration, n.d.).

A **mechanism** explains how a process occurs; a **correlation** describes an association. **Causal inference** concerns whether a change in one factor contributes to a change in another, rather than merely accompanying it. **Translation** connects research evidence to a defined application and tests whether that application is justified. These working distinctions organise the chapter's methodological discussion; they are not competing diagnoses or distinct biological substances.''')
sections={
'1.3':'''## 1.3 History of stress science

### 1.3.1 Internal regulation and emergency responses

Claude Bernard's account of the internal environment provided an important foundation for physiological explanations of regulation. Walter Cannon developed the concept of homeostasis and examined coordinated responses to threats. His work linked sympathetic and adrenal responses to the mobilisation of the organism for action, helping establish the framework commonly described as fight or flight. The intellectual shift was from considering organs in isolation towards asking how coordinated physiological adjustments preserve function under changing conditions (Goldstein & Kopin, 2007; Godoy et al., 2018).

Homeostasis did not imply immobility. Its explanatory value lay in showing how stability depends on compensatory processes. A controlled variable can be maintained within a viable range while the activity of the mechanisms regulating it changes. This distinction remains essential when interpreting a hormone or autonomic measure: a changed effector signal does not necessarily mean that regulation has failed (Goldstein & Kopin, 2007).

### 1.3.2 Selye and subsequent revisions

Hans Selye's 1936 work helped establish a biological research programme concerned with recurring responses to different harmful agents. His general adaptation syndrome described alarm, resistance, and exhaustion. The framework gave prominence to coordinated bodily responses and the potential consequences of sustained demands, but its claim to nonspecificity should be understood as a historical proposition rather than an assumption that every stressor produces the same response in every person (Godoy et al., 2018; Goldstein & Kopin, 2007).

Subsequent systems accounts emphasise patterned responses that depend on the challenge, the organism's interpretation, and its history. Allostasis extends the discussion to changing regulatory demands and anticipatory adjustments, while allostatic load directs attention to cumulative burden. Neither term removes the need to identify the particular process and time scale under investigation. Historical models are most useful when they generate testable questions, not when their vocabulary substitutes for measurement (Goldstein & Kopin, 2007; Godoy et al., 2018).

The implications for trauma research are methodological as well as conceptual. A study must distinguish the event, the measured response, and its interpretation. The existence of a stress response does not establish a psychiatric disorder, while the absence of a proposed laboratory pattern does not invalidate a person's experience. General stress physiology and the neurobiology of a particular disorder are related fields, not identical explanatory systems.

''',
'1.4':'''## 1.4 Early lesion and behavioural studies

Lesion research contributes to neuroscience by examining function after damage or removal of tissue. Scoville and Milner's 1957 report of memory impairment following bilateral medial temporal surgery is a foundational example. Their observations linked extensive damage involving the hippocampal region to persistent difficulty retaining recent experience. The report also distinguished memory impairment from a uniform loss of general intellectual functioning (Scoville & Milner, 1957).

The significance of this work lies partly in the specificity of the question: which aspects of memory were affected, and how did the pattern relate to the extent of the lesion? It did not demonstrate that memory resided in one isolated point or that all forms of memory were lost. The original authors explicitly considered uncertainty about the contribution of neighbouring structures because the operations did not isolate the hippocampus from all adjacent tissue. Anatomy, behavioural testing, and limits of the intervention therefore had to be interpreted together (Scoville & Milner, 1957).

For trauma neurobiology, this history illustrates how evidence about learning and memory can inform a mechanistic framework without directly establishing the cause of a clinical condition. Findings from neurosurgical lesions are not observations of trauma exposure or PTSD. Applying them to traumatic memory requires additional evidence appropriate to the population and question. Likewise, experimental tasks may isolate a learning process without reproducing the personal and social circumstances of an overwhelming event.

The methodological lesson is not that lesion findings are uninformative, but that their explanatory reach must be specified. Readers should identify the affected tissue, the measured function, the comparison, and plausible alternative interpretations before extending a finding to a broader theory of memory or behaviour.

''',
'1.5':'''## 1.5 Rise of psychophysiology

Psychophysiological research connects psychological tasks or experiences with recorded bodily responses. In trauma research, this approach made it possible to investigate responding to trauma-related cues rather than rely only on retrospective descriptions. Pitman and colleagues' 2012 review identified heart-rate, skin-conductance, and facial electromyographic responses during trauma-related imagery and cue exposure as important parts of the biological PTSD literature. These measures concern different aspects of responding and should not be treated as interchangeable indicators (Pitman et al., 2012).

The development of this approach shifted the question from whether a person reports distress to how recorded responses vary with cues, experimental conditions, and comparison groups. Its value is analytical: a defined task and recording method make a proposed relationship open to observation and criticism. It does not follow that physiological reactivity is a unique signature of a particular event or a stand-alone diagnostic test. A response observed under one laboratory condition cannot simply be generalised to every setting or every individual with the same diagnosis (Pitman et al., 2012).

Interpretation requires attention to what the measure represents, the recording conditions, timing, health, medication, and alternative influences. Comparison with interviews, behavioural tasks, or imaging needs an explicit rationale. Concordance should be demonstrated rather than assumed. Psychophysiology therefore complements other methods: it adds measurable information while leaving the researcher responsible for showing what conclusions the task and comparison can support.

''',
'1.6':'''## 1.6 Development of neuroendocrinology

Neuroendocrinology developed through work on communication between the nervous and endocrine systems and through advances that made very small quantities of hormones measurable. The 1977 Nobel account highlights two complementary achievements: Roger Guillemin and Andrew Schally's work on hypothalamic releasing hormones, and Rosalyn Yalow's development of radioimmunoassay with Solomon Berson. Identifying regulatory substances and measuring them were distinct but mutually important steps (Karolinska Institutet, 1977).

The same account records the establishment of the structure of thyrotropin-releasing factor in 1969. This is an example of how a proposed regulatory influence became a chemically characterised signal. Sensitive assays also changed the kinds of questions that could be asked about hormone secretion and disease. These developments supported a research programme in which neural regulation could be investigated through defined endocrine signals rather than inferred only from outward behaviour (Karolinska Institutet, 1977).

Stress research draws on the hypothalamic–pituitary–adrenal axis alongside sympathetic and other regulatory processes. The importance of endocrine regulation does not imply that every form of traumatic stress involves the same hormonal pattern. Pitman and colleagues specifically cautioned that a simple model of chronically increased hypothalamic–pituitary–adrenal activity does not characterise PTSD. General models of stress must therefore be tested rather than transferred uncritically to a clinical diagnosis (Godoy et al., 2018; Pitman et al., 2012).

A hormone result is meaningful only in relation to the sampling conditions, timing, assay, comparison, and question. Health, medication, sleep, and repeated sampling can affect interpretation. Historical advances in assay sensitivity expanded measurement; they did not remove the need for defensible study design or convert a laboratory value into an independent account of an individual's experience.

''',
'1.7':'''## 1.7 Growth of brain imaging

Imaging expanded trauma research beyond peripheral physiological and endocrine measures to investigation of brain structure and function. Hinojosa and colleagues locate the early PTSD neuroimaging literature in the 1990s and describe the subsequent expansion of work on vulnerability, change after exposure, treatment outcomes, and proposed brain-based subgroups. The change in method opened new questions; it did not make biological interpretation independent of study design (Hinojosa et al., 2024).

One central problem is temporal order. A difference measured after exposure may have preceded the event, followed it, or reflect factors related to both exposure and outcome. Cross-sectional group comparisons alone cannot resolve these possibilities. The 2024 review therefore emphasises prospective longitudinal designs with measurements before exposure and at follow-up, as well as replication of proposed subgroups. It also distinguishes progress in research from implementation in routine clinical practice (Hinojosa et al., 2024).

Earlier synthesis had already connected PTSD research to hippocampal, amygdala, cingulate, and prefrontal findings while noting uncertainty about whether some differences represented vulnerability or acquired change. Such findings should be read as claims about specified samples and measures, not as a universal map of a traumatised brain. Regional findings can help formulate hypotheses about memory, threat, and regulation, but a group pattern does not determine a person's diagnosis or establish a particular history (Pitman et al., 2012).

The historical progression from peripheral recording to imaging is therefore not a progression from subjective evidence to an infallible biological answer. It is an expansion of observable information that brings new demands for measurement quality, appropriate comparison, temporal design, reproducibility, and restraint in clinical inference (Hinojosa et al., 2024).

'''
}
for key,body in sections.items():
 nextnum=str(int(key.split('.')[1])+1)
 pat=rf'## {re.escape(key)} [\s\S]*?(?=## 1\.{nextnum} )'
 s,count=re.subn(pat,lambda m:body,s,count=1);assert count==1,key
s=s.replace('The historical topics introduced here require further source-based development before the chapter can fulfil the scope promised by its title. That limitation does not invalidate the methodological framework; it identifies the work still needed for a complete textbook chapter.','The history of the field shows why methodological advances require conceptual discipline. Improved measurement creates opportunities for more precise questions; it does not remove uncertainty about causation, individual interpretation, or appropriate use.')
a=s.index('## Source bibliography retained for verification')
s=s[:a]+'''## References

[BIBLIOGRAPHY]
'''
p.write_text(s)
refs=[
'Godoy, L. D., Rossignoli, M. T., Delfino-Pereira, P., Garcia-Cairasco, N., & de Lima Umeoka, E. H. (2018). A comprehensive overview on stress neurobiology: Basic concepts and clinical implications. Frontiers in Behavioral Neuroscience, 12, Article 127. https://doi.org/10.3389/fnbeh.2018.00127',
'Goldstein, D. S., & Kopin, I. J. (2007). Evolution of concepts of stress. Stress, 10(2), 109–120. https://doi.org/10.1080/10253890701288935',
'Hinojosa, C. A., George, G. C., & Ben-Zion, Z. (2024). Neuroimaging of posttraumatic stress disorder in adults and youth: Progress over the last decade on three leading questions of the field. Molecular Psychiatry, 29(10), 3223–3244. https://doi.org/10.1038/s41380-024-02558-w',
'Karolinska Institutet. (1977, October). The Nobel Prize in Physiology or Medicine 1977 [Press release]. NobelPrize.org. https://www.nobelprize.org/prizes/medicine/1977/press-release/',
'Pitman, R. K., Rasmusson, A. M., Koenen, K. C., Shin, L. M., Orr, S. P., Gilbertson, M. W., Milad, M. R., & Liberzon, I. (2012). Biological studies of post-traumatic stress disorder. Nature Reviews Neuroscience, 13(11), 769–787. https://doi.org/10.1038/nrn3339',
'Scoville, W. B., & Milner, B. (1957). Loss of recent memory after bilateral hippocampal lesions. Journal of Neurology, Neurosurgery, and Psychiatry, 20(1), 11–21. https://doi.org/10.1136/jnnp.20.1.11',
'U.S. Food and Drug Administration. (n.d.). About biomarkers and qualification. https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification'
]
Path('manuscript/chapter01-verified-references.json').write_text(json.dumps(refs,indent=2,ensure_ascii=False))
print('Reconstructed sections 1.3–1.7; added definitions and seven cited reference records.')
