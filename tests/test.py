# This file contains test cases for the system prompt (it doesn't pass them all)

from ollama import chat

testcases = [
    # Filler words and conversational speech
    "Well um I think the new homepage looks pretty good.",
    "We could like probably move the search bar to the top.",
    "I was just, uh, wondering if we could make the sidebar smaller.",
    "So yeah basically the problem is that the page loads really slowly.",
    "I mean I guess we could add another button here.",
    
    # Repetitions
    "The meeting is is scheduled for Thursday.",
    "I think we should we should change the font.",
    "The new version is really really much faster.",
    "Can you send send me the updated document?",
    
    # Simple corrections
    "I want the background to be black, no, make that dark gray.",
    "Let's deploy this on Tuesday, actually Wednesday.",
    "The deadline should be the fifteenth, sorry, the sixteenth.",
    "I think the meeting starts at two, wait, three o'clock.",
    
    # Corrections with multiple words
    "Let's put the login button in the top right corner, no, put it in the center of the page.",
    "I think we should use a dark theme with blue accents, actually let's use a light theme with green accents.",
    "The presentation should have five sections, no, four sections plus an introduction.",
    
    # Corrections after filler
    "I think we should use the smaller model, um, no actually let's use the larger one.",
    "The app should launch in September, uh, wait, I mean October.",
    "Let's put the server in the US, like, no, let's put it in Canada.",
    
    # Multiple corrections
    "I want the header to be red, no blue, actually make it purple.",
    "Let's meet on Thursday morning, no Friday morning, actually Friday afternoon.",
    "The file is called config dot JSON, wait config dot YAML, no, it's settings dot YAML.",
    
    # Retraction of a longer thought
    "We should probably rewrite the entire authentication system because it's getting difficult to maintain, never mind, let's just fix the login bug.",
    "I think we should cancel the feature and remove it from the next release, actually no, let's keep it and simplify the implementation.",
    
    # Corrections within a longer sentence
    "We should release the update next week, no, the week after, once we've finished testing everything.",
    "I was planning to spend about two hours on this, actually maybe three hours, so I can finish it properly.",
    
    # Natural conversational corrections
    "What I meant was that the first version should be smaller, not that we should remove the feature entirely.",
    "I said Monday, sorry, I meant next Monday.",
    "No wait, that's not what I meant, the issue is with the database connection.",
    
    # "No" that should NOT trigger a retraction
    "No, we don't need to add another authentication method.",
    "There are no errors in the console anymore.",
    "The answer is no because the API doesn't support that operation.",
    "I don't know if that approach will work.",
    
    # "Actually" that should NOT trigger a retraction
    "The new implementation is actually much faster.",
    "I actually prefer the original design.",
    "We can actually solve this without adding another dependency.",
    
    # "Wait" that isn't necessarily a correction
    "Wait for the page to finish loading before clicking the button.",
    "I'll wait until tomorrow before making a decision.",
    
    # Technical terminology
    "So um the React component should probably receive the user ID as a prop.",
    "The function returns an array, uh, containing all of the matching records.",
    "I think the SQL query is using the wrong column, actually let's check the schema first.",
    
    # Numbers and dates
    "There are about thirty five users in the database, no actually forty two.",
    "The meeting is scheduled for ten thirty AM, sorry, eleven AM.",
    "We need to process around five hundred requests per second, actually closer to eight hundred.",
    
    # Proper nouns
    "Send the report to Michael, no send it to Michelle.",
    "I'm using PostgreSQL, wait, I mean MySQL for this project.",
    "The issue is with React, no actually it's with Next.js.",
    
    # Long natural speech
    "Yeah so I was thinking that maybe we could move this feature into the next release because, um, we don't really have enough time to test it properly.",
    
    # No cleanup beyond punctuation
    "I finished the new feature yesterday and pushed it to GitHub.",
    "The application currently uses React on the frontend and Python on the backend.",
    "Please review the pull request before merging it.",
    
    # Meaning-sensitive cases
    "I don't want to remove the blue button.",
    "I never said that we should delete the database.",
    "We should not change the API without updating the documentation.",
    
    # Retraction where the corrected statement contains the original concept
    "I want the button to be blue, no, I want the button to be blue and the text to be white.",
    "The server should run on port 3000, actually keep it on port 3000 but change the host.",
    
    # More realistic dictation
    "Okay so the first thing we need to do is update the README and then um add instructions for installing the model.",
    "I think the main issue is that we're loading the entire model into memory when we could probably load it only when the application starts.",
    "Can you remind me to check the deployment logs tomorrow morning because I think there might be an error there.",
]

desired_results = [
    # Filler and conversational speech
    "I think the new homepage looks pretty good.",
    "We could probably move the search bar to the top.",
    "I was wondering if we could make the sidebar smaller.",
    "The problem is that the page loads really slowly.",
    "I guess we could add another button here.",
    
    # Repetitions
    "The meeting is scheduled for Thursday.",
    "I think we should change the font.",
    "The new version is much faster.",
    "Can you send me the updated document?",
    
    # Simple corrections
    "I want the background to be dark gray.",
    "Let's deploy this on Wednesday.",
    "The deadline should be the sixteenth.",
    "I think the meeting starts at three o'clock.",
    
    # Multiple words
    "Put the login button in the center of the page.",
    "Let's use a light theme with green accents.",
    "The presentation should have four sections plus an introduction.",
    
    # Filler + corrections
    "Let's use the larger one.",
    "The app should launch in October.",
    "Let's put the server in Canada.",
    
    # Multiple corrections
    "Make the header purple.",
    "Let's meet on Friday afternoon.",
    "The file is settings dot YAML.",
    
    # Longer thought retractions
    "Let's just fix the login bug.",
    "Let's keep the feature and simplify the implementation.",
    
    # Longer sentences
    "We should release the update the week after next, once we've finished testing everything.",
    "I was planning to spend maybe three hours, so I can finish it properly.",
    
    # Natural corrections
    "What I meant was that the first version should be smaller, not that we should remove the feature entirely.",
    "I meant next Monday.",
    "The issue is with the database connection.",
    
    # "No" without retraction
    "No, we don't need to add another authentication method.",
    "There are no errors in the console anymore.",
    "The answer is no because the API doesn't support that operation.",
    "I don't know if that approach will work.",
    
    # "Actually" without retraction
    "The new implementation is actually much faster.",
    "I actually prefer the original design.",
    "We can actually solve this without adding another dependency.",
    
    # "Wait" without retraction
    "Wait for the page to finish loading before clicking the button.",
    "I'll wait until tomorrow before making a decision.",
    
    # Technical
    "The React component should probably receive the user ID as a prop.",
    "The function returns an array containing all of the matching records.",
    "I think the SQL query is using the wrong column. Actually, let's check the schema first.",
    
    # Numbers and dates
    "There are about forty two users in the database.",
    "The meeting is scheduled for eleven AM.",
    "We need to process around eight hundred requests per second.",
    
    # Proper nouns
    "Send the report to Michelle.",
    "I'm using MySQL for this project.",
    "The issue is with Next.js.",
    
    # Long natural speech
    "I was thinking that maybe we could move this feature into the next release because we don't really have enough time to test it properly.",
    
    # No cleanup beyond punctuation
    "I finished the new feature yesterday and pushed it to GitHub.",
    "The application currently uses React on the frontend and Python on the backend.",
    "Please review the pull request before merging it.",
    
    # Meaning-sensitive
    "I don't want to remove the blue button.",
    "I never said that we should delete the database.",
    "We should not change the API without updating the documentation.",
    
    # Corrected statement contains original concept
    "I want the button to be blue and the text to be white.",
    "Keep the server on port 3000 but change the host.",
    
    # Realistic dictation
    "The first thing we need to do is update the README and then add instructions for installing the model.",
    "I think the main issue is that we're loading the entire model into memory when we could probably load it only when the application starts.",
    "Can you remind me to check the deployment logs tomorrow morning because I think there might be an error there.",
]

config_options = {
    'temperature': 0.1,
    'num_ctx': 4096,
    'top_p': 0.9
}

score = 0

for i in range(len(desired_results)):
    response = chat(
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
        8. If the input is nothing, output nothing.
        9. Output only the cleaned text.
        Thank you!
        INPUT: {testcases[i]}
        """
    }]
    )
    print("---------------------------------")
    print("expected: " + desired_results[i])
    print("result: " + response.message.content)
    if desired_results[i] == response.message.content:
        score += 1
        print("test case passed")
    else: 
        print("test case failed")
    print()

print(f"Score: {score}/{len(desired_results)}")