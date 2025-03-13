import re
from typing import List, Dict, Any
from ..core.factory import create_text_generation_tool
from ..core.registry import registry

# System prompt for YouTube script generation
youtube_script_system_prompt = """
You are a YouTube creator who is creating video scripts that follows:
- informative tone
- Knowledge Gap add in first 30 seconds
- Mystery
- Preview Hook
- call to action
You are creating the video scripts on the keyword asked by the user.
The format should be:

(Start with a mystery)
(Add a knowledge gap)
(Include a preview hook)
(Call to action)

After you finish with the script, please craft 12 compelling hooks. They can be in the form of a question, strong statement, story, or an interesting statistic. Try to provide 3 of each type for variety. Ensure each hook aligns with the essence of the video title.

Then, craft 5 input bias variations that highlight the effort and research put into the video's content.

Finally, think of ten open loop questions that a viewer might have in mind before clicking on the video. These questions should be based on the content implied by the video title.
"""

# User prompt template for YouTube script generation
youtube_script_user_prompt_template = """
Generate a YouTube script for a video about: {topic}.

Please structure the output as follows:

SCRIPT:
[Your generated script here]

HOOKS x12:
[Hook 1]: (Question hook)
[Hook 2]: (Strong statement hook)
[Hook 3]: (Story hook)
[Hook 4]: (Interesting statistical hook)
... (continue for all 12 hooks)

INPUT BIAS x5:
[Input Bias 1]:
[Input Bias 2]:
[Input Bias 3]:
[Input Bias 4]:
[Input Bias 5]:

OPEN LOOP QUESTIONS x10:
[Open Loop Question 1]:
[Open Loop Question 2]:
... (continue for all 10 questions)
"""

# Post-processing function for YouTube scripts
def process_youtube_script(text: str) -> List[str]:
    # Initialize result structure
    script = ""
    hooks = []
    input_bias = []
    open_loop_questions = []
    
    # Extract script section
    script_match = re.search(r'SCRIPT:(.*?)(?=HOOKS|$)', text, re.DOTALL)
    if script_match:
        script = script_match.group(1).strip()
    
    # Extract hooks
    hooks_match = re.search(r'HOOKS.*?:(.*?)(?=INPUT BIAS|$)', text, re.DOTALL)
    if hooks_match:
        hooks_text = hooks_match.group(1)
        # Extract individual hooks
        hook_matches = re.findall(r'\[Hook \d+\].*?:(.*?)(?=\[Hook \d+\]|$)', hooks_text, re.DOTALL)
        if not hook_matches:
            # Try alternative format
            hook_matches = re.findall(r'\d+\.(.*?)(?=\d+\.|$)', hooks_text, re.DOTALL)
        
        hooks = [hook.strip() for hook in hook_matches if hook.strip()]
    
    # Extract input bias
    bias_match = re.search(r'INPUT BIAS.*?:(.*?)(?=OPEN LOOP|$)', text, re.DOTALL)
    if bias_match:
        bias_text = bias_match.group(1)
        # Extract individual input bias statements
        bias_matches = re.findall(r'\[Input Bias \d+\].*?:(.*?)(?=\[Input Bias \d+\]|$)', bias_text, re.DOTALL)
        if not bias_matches:
            # Try alternative format
            bias_matches = re.findall(r'\d+\.(.*?)(?=\d+\.|$)', bias_text, re.DOTALL)
        
        input_bias = [bias.strip() for bias in bias_matches if bias.strip()]
    
    # Extract open loop questions
    questions_match = re.search(r'OPEN LOOP QUESTIONS.*?:(.*?)(?=$)', text, re.DOTALL)
    if questions_match:
        questions_text = questions_match.group(1)
        # Extract individual questions
        question_matches = re.findall(r'\[Open Loop Question \d+\].*?:(.*?)(?=\[Open Loop Question \d+\]|$)', questions_text, re.DOTALL)
        if not question_matches:
            # Try alternative format
            question_matches = re.findall(r'\d+\.(.*?)(?=\d+\.|$)', questions_text, re.DOTALL)
        
        open_loop_questions = [question.strip() for question in question_matches if question.strip()]
    
    # If we couldn't extract structured content, return the full text as the script
    if not script and not hooks and not input_bias and not open_loop_questions:
        return [text.strip()]
    
    # Combine all sections into a list of lines
    result = []
    
    if script:
        result.append("SCRIPT:")
        result.append(script)
        result.append("")
    
    if hooks:
        result.append("HOOKS:")
        for i, hook in enumerate(hooks, 1):
            result.append(f"{i}. {hook}")
        result.append("")
    
    if input_bias:
        result.append("INPUT BIAS:")
        for i, bias in enumerate(input_bias, 1):
            result.append(f"{i}. {bias}")
        result.append("")
    
    if open_loop_questions:
        result.append("OPEN LOOP QUESTIONS:")
        for i, question in enumerate(open_loop_questions, 1):
            result.append(f"{i}. {question}")
    
    return result

# Define custom tips and benefits for the YouTube script generator
youtube_script_tips = [
    "Start with a strong hook to grab attention",
    "Include a knowledge gap in the first 30 seconds",
    "Use a preview hook to keep viewers watching",
    "Maintain an informative tone throughout",
    "End with a clear call to action",
    "Use open loop questions to create curiosity"
]

youtube_script_benefits = [
    "Save time on script writing and content planning",
    "Create more engaging and viewer-retaining content",
    "Develop multiple hooks to test and optimize",
    "Establish credibility with input bias statements",
    "Generate curiosity with open loop questions"
]

# Create the YouTube script generator tool
YoutubeScriptGeneratorClass = create_text_generation_tool(
    name="YouTube Script Generator",
    description="Create engaging YouTube video scripts with hooks, input bias, and open loop questions.",
    icon="""<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
    </svg>""",
    system_prompt=youtube_script_system_prompt,
    user_prompt_template=youtube_script_user_prompt_template,
    input_form_fields={
        "topic": {
            "type": "textarea",
            "label": "What's your YouTube video about?",
            "placeholder": "Describe your video topic in detail for better results...",
            "required": True,
            "rows": 3
        }
    },
    post_process_func=process_youtube_script
)

# Add custom tips and benefits
YoutubeScriptGeneratorClass.tips = youtube_script_tips
YoutubeScriptGeneratorClass.benefits = youtube_script_benefits

# Instantiate the tool
youtube_script_generator_tool = YoutubeScriptGeneratorClass()

# Register the tool with the registry
registry.register(youtube_script_generator_tool, categories=["Content Creation"])
