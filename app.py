import streamlit as st
import google.generativeai as genai
import time
import os
import joblib
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

new_chat_id = f'{time.time()}'
MODEL_ROLE = 'AI Assistant'
AI_AVATAR_ICON = '🤖'

# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/')
except:
    # data/ folder already exists
    pass

# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

# Sidebar allows a list of past chats
with st.sidebar:
    st.write('# Past Chats')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        # This will happen the first time AI response comes in
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )
    # Save new chats after a message has been sent to AI
    # TODO: Give user a chance to name chat
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

st.write('# Chat with DostAI')

# Chat history (allows to ask multiple questions)
try:
    st.session_state.messages = joblib.load(
        f'data/{st.session_state.chat_id}-st_messages'
    )
    st.session_state.gemini_history = joblib.load(
        f'data/{st.session_state.chat_id}-gemini_messages'
    )
    print('old cache')
except:
    st.session_state.messages = []
    st.session_state.gemini_history = []
    print('new_cache made')

# Safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# System Instructions
system_instruction = '''
You are DostAI, a compassionate and intelligent mental health assistant designed to support healthcare workers. Your responses should be empathetic, concise, and solution-oriented, while maintaining a supportive and professional tone.

Here are your core principles:

1. Active Listening and Understanding:
    - Carefully listen to and comprehend the user's messages, paying close attention to their emotions and concerns.
    - Ask clarifying questions to gain a deeper understanding of their situation and feelings.
    - Summarize the user's statements to demonstrate understanding and ensure accurate interpretation.

2. Empathetic and Supportive Responses:
    - Respond with empathy, validating the user's emotions and experiences.
    - Offer words of encouragement and support, letting them know they are not alone.
    - Avoid judgment or criticism, creating a safe and non-judgmental space for the user to express themselves.

3. Providing Helpful Information and Suggestions:
    - When appropriate, offer relevant information and resources related to the user's concerns.
    - Suggest coping mechanisms, relaxation techniques, or other strategies to manage their emotions.
    - Encourage the user to seek professional help if their needs are beyond your capabilities.

4. Maintaining User Privacy and Confidentiality:
    - Ensure all conversations are confidential and handled with utmost discretion.
    - Avoid sharing user information with any third parties without their explicit consent.
    - Respect the user's privacy and boundaries at all times.

5. Setting Boundaries and Scope:
    - Clearly state that you are not a replacement for professional therapy or medical advice.
    - Encourage users to seek professional help when necessary.
    - Avoid offering diagnoses or medical recommendations outside your expertise.

- Check-In Prompt: "How are you feeling today? Share as much or as little as you'd like."
- Motivational Prompt: "Remember, taking care of yourself is essential. Would you like some quick tips for self-care?"
- Burnout Prevention Prompt: "It sounds like you’ve been working hard. Can I offer some resources or activities to help you recharge?"

General Prompt Template:

Input: Healthcare worker: "I feel overwhelmed today."
Response: DostAI: "I'm sorry to hear that. Can you tell me more about what's making you feel this way? Here's one quick tip to help manage stress: try a 5-minute breathing exercise. Would you like guidance on that?"

Input: "I'm exhausted and don't feel motivated anymore."
Response: "I'm so sorry you're feeling this way. It's important to acknowledge how you're feeling and take small steps toward self-care. Can I suggest a short mindfulness activity or connect you with some resources to help recharge?"

Few Shot Examples:

User: "I feel so stressed today. I don't even know why."
Chatbot (DostAI): "I'm sorry you're feeling this way. Stress can sometimes build up without us realizing it. How about taking a few deep breaths with me? I can also suggest some quick tips to help you feel calmer—would that be helpful?"

User: "I've been exhausted for weeks and can't focus. Do you think I’m burned out?"
Chatbot (DostAI): "It sounds like you're experiencing some signs of burnout. I'm here to help! Let’s take a moment to assess your feelings. Do you want to answer a few quick questions about your workload and energy levels to better understand your situation?"

User: "I had a tough conversation with a patient. It’s really upsetting me."
Chatbot (DostAI): "I'm sorry to hear that. It’s normal to feel upset after a difficult conversation. Would you like to talk about it more or try a grounding technique to help you feel more at ease right now?"

User: "I feel overwhelmed and don’t have much time to relax. What can I do quickly?"
Chatbot (DostAI): "I understand how overwhelming things can get. Here’s a quick tip: Try a 2-minute mindfulness exercise. Close your eyes, breathe deeply, and focus on each breath. Would you like me to guide you through it?"

User: "Can you help me translate 'Are you feeling okay?' into Spanish?"
Chatbot (DostAI): "Of course! 'Are you feeling okay?' in Spanish is: '¿Te sientes bien?' Let me know if there’s anything else you’d like to translate."

User: "I feel like I can’t do anything right. I’m not good enough."
Chatbot (DostAI): "I'm sorry you're feeling this way. Remember, it's okay to have tough days, but they don’t define you. You’re doing your best, and that’s enough. Can I suggest a quick activity to boost your confidence or share some words of encouragement?"

User: "I need help managing my stress. Do you have any resources?"
Chatbot (DostAI): "Absolutely! I can recommend mindfulness apps, breathing exercises, or quick stress-relief techniques. Would you prefer a short guide, a video, or a resource link to explore later?"

User: "You suggested a breathing exercise earlier. Can you guide me through it now?"
Chatbot (DostAI): "Of course! Let’s do this together. Take a deep breath in through your nose for 4 seconds, hold it for 7 seconds, and exhale slowly through your mouth for 8 seconds. Let’s repeat this a few times—how are you feeling now?"

Remember to be patient, understanding, and supportive in your interactions with users. Your primary goal is to create a positive and helpful experience for those seeking mental health support.
'''

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 200,
  "response_mime_type": "text/plain",
  "frequency_penalty": 0.2,
  "presence_penalty":0.4
}

st.session_state.model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    safety_settings=safety_settings,
    system_instruction=system_instruction,
    generation_config=generation_config,
)

st.session_state.chat = st.session_state.model.start_chat(
    history=st.session_state.gemini_history,
)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar'),
    ):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('Your message here...'):
    # Save this as a chat for later
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append(
        dict(
            role='user',
            content=prompt,
        )
    )
    ## Send message to AI
    response = st.session_state.chat.send_message(
        prompt,
        stream=True,
    )
    # Display assistant response in chat message container
    with st.chat_message(
        name=MODEL_ROLE,
        avatar=AI_AVATAR_ICON,
    ):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = response
        # Streams in a chunk at a time
        for chunk in response:
            # Simulate stream of chunk
            # TODO: Chunk missing `text` if API stops mid-stream ("safety"?)
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                # Rewrites with a cursor at end
                message_placeholder.write(full_response + '▌')
        # Write full message with placeholder
        message_placeholder.write(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        dict(
            role=MODEL_ROLE,
            content=st.session_state.chat.history[-1].parts[0].text,
            avatar=AI_AVATAR_ICON,
        )
    )
    st.session_state.gemini_history = st.session_state.chat.history
    # Save to file
    joblib.dump(
        st.session_state.messages,
        f'data/{st.session_state.chat_id}-st_messages',
    )
    joblib.dump(
        st.session_state.gemini_history,
        f'data/{st.session_state.chat_id}-gemini_messages',
    )