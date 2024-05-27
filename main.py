import streamlit as st
import time
import base64
import pdfplumber
import os

st.set_page_config(page_icon=":writing_hand", layout="wide", menu_items={'About': "# Project for data science\n김권호, 박소망찬, 박현우, 이서원, 최진아"})

st.header('Common Application Assistant', divider='rainbow')

prompt_Q = {None : None,
            "Prompt 1" : "Some students have a background, identity, interest, or talent that is so meaningful they believe their application would be incomplete without it. If this sounds like you, then please share your story.",
            "Prompt 2" : "The lessons we take from obstacles we encounter can be fundamental to later success. Recount a time when you faced a challenge, setback, or failure. How did it affect you, and what did you learn from the experience?",
            "Prompt 3" : "Reflect on a time when you questioned or challenged a belief or idea. What prompted your thinking? What was the outcome?",
            "Prompt 4" : "Reflect on something that someone has done for you that has made you happy or thankful in a surprising way. How has this gratitude affected or motivated you?",
            "Prompt 5" : "Discuss an accomplishment, event, or realization that sparked a period of personal growth and a new understanding of yourself or others.",
            "Prompt 6" : "Describe a topic, idea, or concept you find so engaging that it makes you lose all track of time. Why does it captivate you? What or who do you turn to when you want to learn more?",
            "Prompt 7" : "Share an essay on any topic of your choice. It can be one you've already written, one that responds to a different prompt, or one of your own design."}

keys = ["option", "selected", "submitted"]
default_values = [None, False, False]
for key, default_value in zip(keys, default_values):
    if key not in st.session_state:
        st.session_state[key] = default_value

# def extract_data(feed):
#     data = []
#     with pdfplumber.open(feed) as pdf:
#         pages = pdf.pages
#         for p in pages:
#             a = p.extract_text()
#             data.append(a)
#     return data

with st.sidebar:
    if st.session_state["option"] != None:
        st.write(f"{st.session_state["option"]} : {prompt_Q[st.session_state["option"]]}")
    reset =  st.button("Reset")
    if reset:
        st.session_state["option"] = None
        st.session_state["selected"] = False
        st.session_state["submitted"] = False
    GPA = 0
    GPA = st.select_slider(
         "Unweighted GPA",
         options = [x/10 for x in range(10, 41)],
         value = 3.0
    )
    mathe,verbal = st.columns([1,1])
    with mathe:
         SAT_m = st.select_slider(
            "SAT math",
            options = range(200,801,10),
            value = 720
         )
    with verbal:
         SAT_v = st.select_slider(
            "SAT verbal",
            options = range(200,801,10),
            value = 690
         )
    uploaded_files = st.file_uploader("Import your CV.pdf file", accept_multiple_files=True, type="pdf")
    for uploaded_file in uploaded_files:
        with open(f"./{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        # df = extract_data(uploaded_file)
        # st.write(df)
        

col1, col2 = st.columns([1,1])
with col1:
    if st.session_state["submitted"]:
        with st.container():
             # st.write_Stream 참고하면 재밌을듯
             st.write(st.session_state["submitted"])
    else:
        st.write("Step 1: Choose your Common app Prompt type")
        cola, colb = st.columns([5,1])
        with cola:
            st.session_state["option"] = st.selectbox(
            "Choose your Common app Prompt type.", ("Prompt 1", "Prompt 2", "Prompt 3", "Prompt 4", "Prompt 5", "Prompt 6", "Prompt 7"),
            index=None, placeholder="Select prompt type...",
            label_visibility="collapsed"
            )
        with colb:
            selected = st.button("Run")
            if selected:
                st.session_state["selected"] = True
        if st.session_state["selected"]:
            st.write("Step 2: Fill in the form")
            match st.session_state["option"]:
                case "Prompt 1":
                    with st.form("prompt_1"):
                        st.subheader("Characteristic")
                        characteristic = st.multiselect(
                            'Select up to 3 characteristic which you want to emphasize yourself.',
                            ['Kind', 'Sincere', 'Persistent', 'Open-minded', 'Fair', 'Optimistic', 'Enthusiastic', 'diligent', 'outgoing', 'responsible'],
                            ['diligent', 'outgoing', 'responsible'])
                        st.subheader("Anecdote / episode")
                        epi = st.text_area(
                            "Describe an event that affected your personality or the formation of your values.",
                            label_visibility="visible",
                            disabled=False,
                            value="When I was in elementary school, I was bullied, but I made a friend who always took care of me and helped me."
                            )
                        epi_result = st.text_area(
                            "How does it affect you.",
                            label_visibility="visible",
                            disabled=False,
                            value="When I saw someone in another trouble, I first came forward to help, and I learned that I should treat others as much as I want to be treated."
                            )
                        st.subheader("Activities")
                        act = st.text_area(
                            "Describe meaningful extracurricular/club activities that you learned something.",
                            label_visibility="visible",
                            disabled=False,
                            value="I was a vice-captaion of a basketball team in my middle school.\nAlso, I did cooking volunteer work at the orphanage."
                            )
                        act_result = st.text_area(
                            "What did you learn from the activity (Either Performance or Mindset).",
                            label_visibility="visible",
                            disabled=False,
                            value="I learned that when I serve others, I can bring joy not only to the other person, but also to me who does. While serving as the vice-captain of the club, I showed an example of effort, and was able to finish second in the local competition."
                            )
                        st.subheader("Awards")
                        Awards1 = st.text_input(
                            "(Optional) :star: Just list related awards in the context above.",
                            label_visibility="visible",
                            disabled=False,
                            value="MVP in Point Guard at a Regional Basketball Tournament"
                            )
                        Awards2 = st.text_input(
                            "(Optional)",
                            label_visibility="visible",
                            disabled=False
                            )
                        Awards = [x for x in [Awards1, Awards2] if x != ""]

                        submitted = st.form_submit_button("Submit")
                        if submitted:
                            progress_text = "Operation in progress. Please wait."
                            my_bar = st.progress(0, text=progress_text)
                            for percent_complete in range(100):
                                time.sleep(0.01)
                                my_bar.progress(percent_complete + 1, text=progress_text)
                            time.sleep(1)
                            my_bar.empty()

                            st.session_state["submitted"] = {"num_prompt" : 1, "prompt_question" : prompt_Q[st.session_state["option"]],
                                                             "characteristic": characteristic, "episode" : epi, "learning_epi" : epi_result, "activity" : act, "learning_act" : act_result, "Awards": Awards}
                            st.session_state["selected"] = False
                            st.rerun()

                # case "Prompt 5":
                #     with st.form("prompt_5"):
                #         st.write("Inside the form")
                #         slider_val = st.slider("Form slider")
                #         checkbox_val = st.checkbox("Form checkbox")

                #         submitted = st.form_submit_button("Submit")
                #         if submitted:
                #             st.session_state["submitted"] = {"checkbox_val": checkbox_val}
                #             st.session_state["selected"] = False

with col2:
    tab1, tab2, tab3 = st.tabs(["Tips", "feedbacks", "sentence feedbacks"])
    with tab1:
        if st.session_state['option'] == 'Prompt 1':
             st.subheader(":bulb: Tips for Prompt 1")
             st.subheader("How to Highlight Your Background")
             st.write("As an example of a topic, let’s say that a student wrote about how their mother was a henna tattoo artist. They could explain how they learned their own style of henna tattoo design by embracing what their mother taught them and then tweaking it to make it their own. Here we can see the theme of self-exploration. Indeed, any passion that isn’t on your resume or activities list can really give some insight into who you are and what makes you tick. Instead of trying to impress readers by making up unusual or shocking things, think about how you spend your free time. Ask yourself why you spend it that way and how your upbringing, your identity, and your life experiences have shaped who you are.")
             st.write("Background is the central theme behind any response to prompt #1. The background that you have can include long-term interactions with art or music, sciences, sports, writing, and many other learned skills. It also includes your social environments and how they’ve influenced you. In addition, you can highlight intersections between multiple parts of your background or multiple backgrounds in general, and you can show how each one is essential to you.")
             st.subheader("Include an Anecdote")
             st.write("One thing to bring your attention to here is that the essay opens on a story about the author’s parents. \
                      You want to make sure that if you’re going to use this kind of narrative that you make the essay about you as much as possible. You have to show how you are going to be interacting with each character and how it paves the way for your background.")
             st.subheader("Focus on Your Identity")
             st.write("In addition, you have to make sure that you explain context well if you’re talking about any sort of more insular community, whether that’s one related to where you grew up or a small culture you are a part of. Otherwise, it can be difficult for a reader who’s not part of that community to understand the messages and the lessons that you’re trying to impart.")
             st.write("Alternatively, focusing on a dominant personality trait can also make for a compelling theme. For example, if you are extremely outgoing, you could explain how your adventurousness has allowed you to learn from a diverse group of friends and the random situations you find yourself in.")
             st.write("One important thing to note is that the topic of identity can easily lack originality. If you cover a common experience, \
                      like feeling divided between cultures, your essay might not stand out. That’s simply because the admissions officers reading these essays have seen some version of these essays many times, so striking a unique chord is going to be more difficult.")
             st.subheader("Talk About an Interest")
             st.write("Lastly, an interest is another topic you can write about for this prompt. Interests are basically synonymous with activities in this case, but slightly broader. You can say that interests encompass activities in the same way that squares are rectangles, but rectangles aren’t squares.")
             st.write("Participation in an interest is often less organized than in an activity. For instance, you might run cross country as an activity, but cook or paint as an interest. \
                      Writing about an interest is a way to highlight passions that may not come across in the rest of your application. For example, if you’re a wrestler, writing about your interest in standup comedy would be a refreshing addition to your application, \
                      and you should also feel free to use this topic to show what an important activity on your application really means to you.")
        if st.session_state['option'] == 'Prompt 5':
             st.subheader(":bulb: Tips for Prompt 5")
             st.subheader("Making the Prompt Personal")
             st.write("Make sure you’re remembering your audience. Alternatively, a more relaxed way to address this prompt is using an informal event or realization, which could allow you to show more personality and creativity. An example of this could be learning how to bake with your mother, \
                      which sparked a newfound connection with your mom. ")
             st.subheader("Brainstorming and Planning")
             st.write("The key to answering this prompt is clearly defining what it is that sparked your growth, and then describing this spark in detail, going into the nature of this growth and how it relates to your perception of yourself and others around you. \
                      You have to answer or reference this prompt in all parts of the essay, and this is crucial because you have to dedicate sufficient time to the new perception of yourself and others in order to not undersell the description of how you grew and changed.")
    tab2.subheader("overall feedbacks are here.")
    tab3.subheader("sentence-by-sentence feedbacks are here.")
