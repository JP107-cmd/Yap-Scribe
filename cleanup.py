from ollama import chat

def clean_text(text: str, config_options: dict) -> str:
    try:
        cleaned_text = chat(
            model='qwen3:4b-q4_K_M',
            options=config_options,
            think=False,
            messages=[{'role': 'user', 'content': 
                f"""
                ROLE:
                You are a text-cleanup service.
                OBJECTIVE:
                You are to clean up inputted text, removing unnecessary filler words, or any statements followed by a retracting statement, ENSURING THE ORIGINAL MEANING OF THE TEXT IS PRESERVED.
                RULES:
                1. Remove all filler/uncessary words from input such as "like, uh, um, etc.". Note: only remove filler/unnecessary words when they
                serve as conversational filler and do not change the meaning of the text.
                Examples: 
                    "I uh think the button should be blue." should become "I think the button should be blue".
                    "So we should probably move the database logic into its own file, um, and then import it into the main application." should become
                    "We should probably move the database logic into its own file and then import it into the main application."
                2. Add or correct punctuation and capitalization of input so that the output is grammatically correct.
                Examples: 
                    "I think we should use the blue button because it looks better" should be "I think we should use the blue button because it looks better."
                    "Hey John I finished the project can you take a look at it" should be "Hey John, I finished the project. Can you take a look at it?"
                3. When the input retracts, corrects or replaces a previous statement, remove the retracted text and keep only the corrected text. Note: only treat words that often signify retractions (nevermind, no, actually, wait, sorry) as retractions when the context of the entire input signifies that the speaker wishes to correct themselves, not any time when this terminology is used.
                Examples:
                    "I like the colour blue, nevermind I like the colour red." should be "I like the colour red."
                    "I like the colour blue, no red." should be "I like the colour red."
                    "Let's use the blue button, actually let's use the green button." should be "Let's use the green button."
                    "I think we should use blue, no red, actually green." should be "I think we should use green"
                    "The website should have a dark blue background with white text, nevermind, let's make the background light gray." should be "Let's make the background light gray.",
                    "I think we should use the blue button because, well, actually, after thinking about it, I think green would be better." should be "I think we should use the green button"
                    "I think we should launch the website next Friday, no, next Monday, because we still need to finish testing." should be "I think we should launch the website next Monday because we still need to finish testing."
                    Alternatively, the use of no and actually may not signify a retraction ("No, I think the blue button looks better." or "Actually, I think the current design looks pretty good.")
                4. Remove any repetitions seen in natural speech.
                5. Never add any information not present in the input.
                6. Never change the meaning of the input.
                7. Do not rewrite or change the input if no issues with the input (criteria for an issue outlined in previous rules) is observed.
                8. If the input is empty, output nothing.
                8. Output only the cleaned text.
                INPUT: {text}
                """
            }]
            )
        return cleaned_text.message.content
    except Exception as e:
        print(f"An error occurred during text cleanup: {e}")
        return text