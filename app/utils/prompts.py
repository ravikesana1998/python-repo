def skill_development(text):
    prompt = f'''
            Analyze the given text: {text}, dynamically extracting key areas of personal and professional development based on the content. 
            Identify improvements in relevant skills, knowledge, decision-making, collaboration, adaptability, or any other key aspects 
            found in the text. Present each improved area as an emoticon along with a bold subheading, followed by a concise explanation 
            in short sentence for each improved area in a single line in terms of their improvement. Ensure clarity and brevity. 
            Strictly generate the response without an opening statement, main heading, or any other explanation of the generated output. 
            e.g ["🛠️problem-solving: Developed structured approaches to resolving complex challenges.", 
            "🤝teamwork: Strengthened cross-functional collaboration through clear communication."]
            Make sure the generated response should be strictly in list format and contained only the key developements and their explainations with out empty values in the list.
            '''
    return prompt

def hashtags(text):
    prompt = f'''Generate the hashtags in the list format for the following text - {text} through contextual understanding and semantic meaning.
                Make sure the response should not include explainations,opening statments and subheadings or headings.
                Provide the response strictly in list format '''
    return prompt