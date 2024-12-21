# Automated MCQ Generation with LangChain 🔗 and Gemini API 🚀

## Core Logic of Chain-Based Workflow 🔗
This project utilizes **LangChain** framework to create, evaluate, and analyze multiple-choice quizzes (MCQs) in an automated and efficient manner. The workflow is composed of three sequential steps:
### 1. **Quiz Generation 🧠**
- **Purpose:** Generate MCQs based on the input text.
- **Prompt:** The `quiz_generation_prompt` instructs the model to create a specified number of MCQs (e.g., 5) tailored for a specific subject and level.
- **Output:** A JSON-formatted quiz with questions, options, and answers.

### 2. **Quiz Evaluation and Refinement ✍️**
- **Purpose:** Ensure the quiz meets the cognitive and analytical abilities of the target students.
- **Prompt:** The `quiz_evaluation_prompt` refines the quiz by rewriting questions or adjusting the level if necessary.
- **Output:** An updated version of the quiz, optimized for the target audience.

### 3. **Complexity Analysis 🔍**
- **Purpose:** Assess the complexity of the quiz questions in a concise manner.
- **Prompt:** The `complexity_analysis_prompt` provides a brief (max 50 words) analysis of the question difficulty.
- **Output:** A short summary of the quiz's complexity.

### Sequential Workflow 🔄
These three steps are orchestrated using a **SequentialChain**, which:
1. Takes the input text and parameters (e.g., number of questions, subject, level).
2. Executes the generation, evaluation, and analysis in sequence.
3. Passes the output of each step as input to the next, ensuring a smooth workflow.

### Key Parameters 🛠️
- **`text`**: The source text to generate questions.
- **`number`**: Number of MCQs to generate.
- **`subject`**: Subject area for the quiz.
- **`level`**: Desired level for the quiz (e.g., simple).


## How It Works ⚙️
1. The `generate_quiz` function combines all chains into a single **SequentialChain**.
2. The function processes the input text through the three-step workflow.
3. The final output includes:
   - Refined MCQs in JSON format.
   - A brief complexity analysis of the quiz.

Enjoy creating intelligent, tailored quizzes with ease! 💡🎉

Make sure to download the live demo video in assets folder for a step-by-step walkthrough!