# AI & Robotics Engineering — Textbook-Generation Prompts

## Source context

This directory contains **48 textbook-generation prompts** for the **Bachelor of Artificial Intelligence and Robotics Engineering** programme:

- **47 course textbooks** (course codes AI.101 through AI.411), and
- **1 final-year project handbook** (course code AI.450).

Each prompt is stored as a separate Markdown file named by course code (for example, `AI.101-Introduction-to-Artificial-Intelligence.md`). Every prompt ends with the recommended **TEXTBOOK PRODUCTION STANDARD**, appended per the curriculum author's recommendation so that generated books are textbook-quality rather than expanded lecture notes.

The prompts are raw source material for textbook authoring; they are not textbooks themselves. To produce a textbook, a writer (human or AI-assisted) works through one prompt file, following every coverage, pedagogy, practical-work and assessment instruction.

## Preamble from the curriculum document

> Save this first. Absolutely. For a **Bachelor of Artificial Intelligence and Robotics Engineering**, each course should have its **own textbook-generation prompt**, rather than using one generic prompt for all subjects.
>
> The prompts below are designed to make the resulting textbooks **self-explanatory, undergraduate-level, practical, technically rigorous, and suitable as standalone course textbooks**. Each prompt tells the writer what concepts, mathematics, examples, practicals, projects, exercises, and assessment materials to include.
>
> **Common standard for all 47 textbooks.** Each prompt assumes the textbook should:
>
> - Be written specifically for **Bachelor-level AI and Robotics Engineering students**.
> - Progress from **beginner → intermediate → advanced** within the course.
> - Explain technical terms before using them extensively.
> - Use **simple but academically precise English**.
> - Include worked examples, diagrams described in text, tables, algorithms, pseudocode and practical applications.
> - Include **Python/C++/MATLAB/ROS/Arduino/embedded examples where appropriate**.
> - Include practical laboratory exercises.
> - Include end-of-chapter review questions, MCQs, short-answer questions, numerical problems and programming tasks.
> - Include mini-projects and a final course project where appropriate.
> - Relate theory to **real robots, autonomous systems, AI applications and engineering practice**.
> - Avoid superficial treatment or merely listing definitions.
> - Include mathematical derivations where necessary, but explain their engineering meaning.
> - Use current and technically credible references.
> - Clearly distinguish theory, examples, practicals and assessments.
> - Make every chapter understandable even when the student has not consulted another textbook.

## TEXTBOOK PRODUCTION STANDARD (appended to every prompt file)

The full standard below appears at the end of every prompt file in this collection. It converts each per-course prompt into a complete textbook production specification.

> **TEXTBOOK PRODUCTION STANDARD:** Structure the textbook into approximately 10–15 substantial chapters, depending on the breadth of the course. Each chapter must contain:
>
> 1. Chapter title
> 2. Introduction
> 3. Learning objectives
> 4. Prerequisite knowledge
> 5. Core concepts explained progressively
> 6. Definitions of technical terminology
> 7. Worked examples
> 8. Mathematical derivations where applicable
> 9. Algorithms and pseudocode
> 10. Engineering/AI/robotics applications
> 11. Practical laboratory activity
> 12. Programming exercise where appropriate
> 13. Case study
> 14. Common mistakes and troubleshooting
> 15. Chapter summary
> 16. Key terms
> 17. Review questions
> 18. Multiple-choice questions
> 19. Short-answer questions
> 20. Numerical/problem-solving questions
> 21. Programming/design exercises
> 22. Mini-project
> 23. Further reading and references.
>
> Make the textbook **self-contained**. Do not assume that students already understand advanced concepts. When a concept depends on mathematics, programming, electronics, mechanics or another discipline, briefly teach the prerequisite before applying it.
>
> Use realistic engineering scenarios rather than artificial examples wherever possible. Every major theoretical concept should be connected to an actual AI, robotics, automation, embedded-system or autonomous-system application.
>
> Where programming is required, provide complete runnable examples, explain the code line by line where pedagogically useful, explain expected output, identify common errors and provide extension exercises.
>
> Where hardware is involved, explain the components, connections, operating principles, safety considerations and troubleshooting procedures.
>
> Where algorithms are involved, provide the intuition, formal description, pseudocode, complexity analysis, worked example and practical implementation.
>
> Where mathematical equations are involved, define every symbol and explain the physical or computational meaning of the equation.
>
> Maintain a clear distinction between **theory, worked examples, practical laboratory work, case studies and independent exercises**.
>
> Do not merely mention technologies such as Python, C++, ROS, OpenCV, MATLAB, Arduino, Raspberry Pi, TensorFlow or PyTorch. Teach their relevant use within the context of the course.
>
> End the complete textbook with a comprehensive glossary, bibliography, subject index, practical-laboratory index and list of recommended software/hardware tools.
>
> The final manuscript must read like a professionally authored university textbook rather than AI-generated lecture notes. Avoid repetitive chapter structures, repetitive explanations and unnecessary filler. Use varied explanations, authentic engineering examples and technically precise language throughout.

## Course list

| # | Year | Semester | Code | Course | File |
|---:|:---:|:---:|:---|:---|:---|
| 1 | 1 | 1 | AI.101 | Introduction to Artificial Intelligence | `AI.101-Introduction-to-Artificial-Intelligence.md` |
| 2 | 1 | 1 | AI.102 | Robotics Fundamentals | `AI.102-Robotics-Fundamentals.md` |
| 3 | 1 | 1 | AI.103 | Machine Learning | `AI.103-Machine-Learning.md` |
| 4 | 1 | 1 | AI.104 | Computer Vision | `AI.104-Computer-Vision.md` |
| 5 | 1 | 1 | AI.105 | Natural Language Processing | `AI.105-Natural-Language-Processing.md` |
| 6 | 1 | 1 | AI.106 | Control Systems for AI and Robotics | `AI.106-Control-Systems-for-AI-and-Robotics.md` |
| 7 | 1 | 2 | AI.107 | Data Structures and Algorithms for AI and Robotics | `AI.107-Data-Structures-and-Algorithms-for-AI-and-Robotics.md` |
| 8 | 1 | 2 | AI.108 | Digital Signal Processing for AI and Robotics | `AI.108-Digital-Signal-Processing-for-AI-and-Robotics.md` |
| 9 | 1 | 2 | AI.109 | Embedded Systems for AI and Robotics | `AI.109-Embedded-Systems-for-AI-and-Robotics.md` |
| 10 | 1 | 2 | AI.110 | Human-Robot Interaction | `AI.110-Human-Robot-Interaction.md` |
| 11 | 1 | 2 | AI.111 | Neural Networks | `AI.111-Neural-Networks.md` |
| 12 | 1 | 2 | AI.112 | Computer Graphics for AI and Robotics | `AI.112-Computer-Graphics-for-AI-and-Robotics.md` |
| 13 | 2 | 1 | AI.201 | Internet of Things for AI and Robotics | `AI.201-Internet-of-Things-for-AI-and-Robotics.md` |
| 14 | 2 | 1 | AI.202 | Robotic Perception | `AI.202-Robotic-Perception.md` |
| 15 | 2 | 1 | AI.203 | Ethics in Artificial Intelligence and Robotics | `AI.203-Ethics-in-Artificial-Intelligence-and-Robotics.md` |
| 16 | 2 | 1 | AI.204 | Autonomous Systems | `AI.204-Autonomous-Systems.md` |
| 17 | 2 | 1 | AI.205 | Reinforcement Learning | `AI.205-Reinforcement-Learning.md` |
| 18 | 2 | 1 | AI.206 | Computer Architecture for AI and Robotics | `AI.206-Computer-Architecture-for-AI-and-Robotics.md` |
| 19 | 2 | 2 | AI.207 | Mobile Robotics | `AI.207-Mobile-Robotics.md` |
| 20 | 2 | 2 | AI.208 | Artificial Intelligence for Robotics | `AI.208-Artificial-Intelligence-for-Robotics.md` |
| 21 | 2 | 2 | AI.209 | Fuzzy Logic and Intelligent Control | `AI.209-Fuzzy-Logic-and-Intelligent-Control.md` |
| 22 | 2 | 2 | AI.210 | Deep Learning | `AI.210-Deep-Learning.md` |
| 23 | 2 | 2 | AI.211 | Pattern Recognition | `AI.211-Pattern-Recognition.md` |
| 24 | 2 | 2 | AI.212 | Robot Kinematics | `AI.212-Robot-Kinematics.md` |
| 25 | 3 | 1 | AI.301 | Virtual Reality for AI and Robotics | `AI.301-Virtual-Reality-for-AI-and-Robotics.md` |
| 26 | 3 | 1 | AI.302 | Cyber-Physical Systems | `AI.302-Cyber-Physical-Systems.md` |
| 27 | 3 | 1 | AI.303 | Swarm Robotics | `AI.303-Swarm-Robotics.md` |
| 28 | 3 | 1 | AI.304 | Robot Operating Systems and ROS-Based Robotics | `AI.304-Robot-Operating-Systems-and-ROS-Based-Robotics.md` |
| 29 | 3 | 1 | AI.305 | Cognitive Robotics | `AI.305-Cognitive-Robotics.md` |
| 30 | 3 | 1 | AI.306 | Biologically Inspired Robotics | `AI.306-Biologically-Inspired-Robotics.md` |
| 31 | 3 | 2 | AI.307 | Machine Vision | `AI.307-Machine-Vision.md` |
| 32 | 3 | 2 | AI.308 | Intelligent Control Systems | `AI.308-Intelligent-Control-Systems.md` |
| 33 | 3 | 2 | AI.309 | Multi-Robot Systems | `AI.309-Multi-Robot-Systems.md` |
| 34 | 3 | 2 | AI.310 | Robot Localization and Mapping | `AI.310-Robot-Localization-and-Mapping.md` |
| 35 | 3 | 2 | AI.311 | Robotics Planning | `AI.311-Robotics-Planning.md` |
| 36 | 3 | 2 | AI.312 | Social Robotics | `AI.312-Social-Robotics.md` |
| 37 | 4 | 1 | AI.401 | Evolutionary Robotics | `AI.401-Evolutionary-Robotics.md` |
| 38 | 4 | 1 | AI.402 | Robot Ethics and Responsible Robotics | `AI.402-Robot-Ethics-and-Responsible-Robotics.md` |
| 39 | 4 | 1 | AI.403 | Robot Learning | `AI.403-Robot-Learning.md` |
| 40 | 4 | 1 | AI.404 | Artificial Intelligence Ethics | `AI.404-Artificial-Intelligence-Ethics.md` |
| 41 | 4 | 1 | AI.405 | Robot Manipulation | `AI.405-Robot-Manipulation.md` |
| 42 | 4 | 1 | AI.406 | Advanced Robot Perception | `AI.406-Advanced-Robot-Perception.md` |
| 43 | 4 | 2 | AI.407 | Robot Navigation | `AI.407-Robot-Navigation.md` |
| 44 | 4 | 2 | AI.408 | Robot Path Planning | `AI.408-Robot-Path-Planning.md` |
| 45 | 4 | 2 | AI.409 | Robot Simulation | `AI.409-Robot-Simulation.md` |
| 46 | 4 | 2 | AI.410 | Robot Vision | `AI.410-Robot-Vision.md` |
| 47 | 4 | 2 | AI.411 | Robot Design and Engineering | `AI.411-Robot-Design-and-Engineering.md` |
| 48 | 4 | 2 | AI.450 | Artificial Intelligence and Robotics Engineering Project (final-year project handbook) | `AI.450-Artificial-Intelligence-and-Robotics-Engineering-Project.md` |

## Conventions

- File names follow `AI.<code>-<Title-in-Title-Case>.md`.
- Each prompt file reproduces the curriculum text verbatim, followed by the TEXTBOOK PRODUCTION STANDARD block.
- The TEXTBOOK PRODUCTION STANDARD is the curator's recommended addition to every prompt; it is not part of the original per-prompt course text.
