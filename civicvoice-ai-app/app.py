import streamlit as st
from langdetect import detect, LangDetectException
import db
import plotly.express as px
import auth
import openai

# --- App Title ---
db.init_db()
st.title("CivicVoice – AI-Powered Public Issue Reporter")

# --- Welcome Screen State ---
if 'show_welcome' not in st.session_state:
    st.session_state['show_welcome'] = True
if 'show_login_tab' not in st.session_state:
    st.session_state['show_login_tab'] = False
if 'show_signup_tab' not in st.session_state:
    st.session_state['show_signup_tab'] = False

# --- Authentication ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

def show_login(selected_tab=None):
    st.title("CivicVoice Login / Signup")
    tab_labels = ["Login", "Sign Up", "Admin"]
    if selected_tab is not None:
        tab1, tab2, tab3 = st.tabs(tab_labels)
    else:
        tab1, tab2, tab3 = st.tabs(tab_labels)
    with tab1:
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if auth.login_user(login_user, login_pass):
                st.session_state['authenticated'] = True
                st.session_state['username'] = login_user
                auth.log_login(login_user)
                st.success("Login successful!")
                st.session_state['show_admin_dashboard'] = False
                st.rerun()
            else:
                st.error("Invalid username or password.")
    with tab2:
        signup_user = st.text_input("Username", key="signup_user")
        signup_pass = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            if not signup_user or not signup_pass:
                st.error("Please enter a username and password.")
            elif signup_user.lower() == 'admin':
                st.error("Cannot sign up as admin.")
            elif auth.user_exists(signup_user):
                st.error("Username already exists.")
            else:
                auth.signup_user(signup_user, signup_pass)
                st.success("Signup successful! Please log in.")
    with tab3:
        import os
        if not os.path.exists("admin_config.json"):
            st.info("Set admin password (first time setup)")
            new_admin_pass = st.text_input("Set Admin Password", type="password", key="set_admin_pass")
            if st.button("Set Admin Password"):
                if not new_admin_pass:
                    st.error("Please enter a password.")
                else:
                    auth.set_admin_password(new_admin_pass)
                    st.success("Admin password set! Please log in as admin.")
                    st.rerun()
        else:
            admin_pass = st.text_input("Admin Password", type="password", key="admin_login_pass")
            if st.button("Admin Login"):
                if auth.admin_login(admin_pass):
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = 'admin'
                    st.session_state['show_admin_dashboard'] = True
                    auth.log_login('admin')
                    st.success("Admin login successful!")
                    st.rerun()
                else:
                    st.error("Invalid admin password.")

# --- Welcome Screen Logic ---
if not st.session_state['authenticated']:
    if st.session_state['show_welcome']:
        st.header("Welcome to CivicVoice!")
        st.markdown("""
        **Report any problem that you want to report to the government.**
        CivicVoice helps you raise your voice and bring attention to public issues in your area.
        """)
        # Show total problems reported
        total_problems = db.count_submissions()
        st.metric(label="Problems Reported", value=f"{total_problems}")
        # (Removed: problem table)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login"):
                st.session_state['show_welcome'] = False
                st.session_state['show_login_tab'] = True
                st.session_state['show_signup_tab'] = False
                st.rerun()
        with col2:
            if st.button("Sign Up"):
                st.session_state['show_welcome'] = False
                st.session_state['show_login_tab'] = False
                st.session_state['show_signup_tab'] = True
                st.rerun()
        st.markdown("---")
        st.info("Or, if you are an admin, use the Admin tab after proceeding.")
        st.stop()
    else:
        # Show login/signup/admin tabs, defaulting to the selected one
        if st.session_state.get('show_login_tab', False):
            show_login(selected_tab=0)
        elif st.session_state.get('show_signup_tab', False):
            show_login(selected_tab=1)
        else:
            show_login()
        st.stop()
else:
    st.sidebar.write(f"Logged in as: {st.session_state['username']}")
    # Debug: show username and admin check
    st.sidebar.caption(f"(Debug: username='{st.session_state['username']}', admin={st.session_state['username'].lower() == 'admin'})")
    # Show admin dashboard directly if admin and flag is set
    if st.session_state['username'] == 'admin' and st.session_state.get('show_admin_dashboard', False):
        st.header("Admin Dashboard: Submissions Preview & Stats")
        submissions = db.fetch_all_submissions()
        if not submissions:
            st.info("No submissions yet.")
        else:
            import pandas as pd
            import io, json
            df = pd.DataFrame([row[:10] for row in submissions], columns=["id", "issue_text", "language", "location", "consent", "image", "image_caption", "audio", "created_at", "username"])
            st.subheader("All Submissions")
            st.dataframe(df[["created_at", "username", "language", "location", "consent", "issue_text", "image_caption"]])
            # Export buttons (exclude image/audio blobs)
            export_cols = ["created_at", "username", "language", "location", "consent", "issue_text", "image_caption"]
            csv_buffer = io.StringIO()
            df[export_cols].to_csv(csv_buffer, index=False)
            st.download_button("Download CSV", csv_buffer.getvalue(), file_name="submissions.csv", mime="text/csv", key="csv_download")
            json_str = df[export_cols].to_json(orient="records", force_ascii=False)
            st.download_button("Download JSON", json_str, file_name="submissions.json", mime="application/json", key="json_download")
            # Language distribution chart
            lang_counts = df["language"].value_counts().reset_index()
            lang_counts.columns = ["Language", "Count"]
            fig = px.bar(lang_counts, x="Language", y="Count", title="Submissions by Language")
            st.plotly_chart(fig, use_container_width=True)
            # Preview images/audio for first 3 submissions
            st.subheader("Sample Media Preview (first 3)")
            for i, row in df.head(3).iterrows():
                st.markdown(f"**Submission {row['id']} ({row['created_at']}):**")
                if row["image"]:
                    st.image(row["image"], caption=row["image_caption"] or "Uploaded Image", use_column_width=True)
                if row["audio"]:
                    st.audio(row["audio"], format='audio/wav')
                st.write(f"**Text:** {row['issue_text']}")
                st.write(f"**Location:** {row['location']}")
                st.write("---")
            # Map visualization
            from geopy.geocoders import Nominatim
            import folium
            from streamlit_folium import st_folium
            st.subheader("Submission Locations Map")
            geolocator = Nominatim(user_agent="civicvoice-app")
            m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)  # Center on India
            mapped = 0
            unmapped = 0
            for loc, text in zip(df["location"], df["issue_text"]):
                try:
                    geo = geolocator.geocode(loc, timeout=5)
                    if geo:
                        folium.Marker([geo.latitude, geo.longitude], popup=text).add_to(m)
                        mapped += 1
                    else:
                        unmapped += 1
                except Exception:
                    unmapped += 1
            st_folium(m, width=700, height=400)
            if unmapped > 0:
                st.warning(f"{unmapped} locations could not be mapped.")
            # Placeholder for Folium map
            st.caption("(Future: Map visualization of locations)")

# --- Language Selection ---
languages = [
    ("en", "English"),
    ("hi", "Hindi"),
    ("ta", "Tamil"),
    ("te", "Telugu"),
    ("bn", "Bengali"),
    ("ml", "Malayalam"),
    ("kn", "Kannada"),
    ("mr", "Marathi"),
    ("gu", "Gujarati"),
    ("pa", "Punjabi"),
    ("or", "Odia"),
    ("as", "Assamese"),
    ("ur", "Urdu"),
    ("other", "Other")
]
language_codes = [code for code, name in languages]
language_names = [name for code, name in languages]

st.subheader("Select Input Language")
language_mode = st.radio("How would you like to select the language?", ["Manual", "Auto-detect"])

selected_language = None
if language_mode == "Manual":
    selected_language = st.selectbox("Choose your language", language_names)
else:
    st.info("Language will be auto-detected from your input.")

# --- OpenAI API Key ---
openai.api_key = "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"

# --- Problem Categories ---
CATEGORIES = [
    "Roads/Transport",
    "Water",
    "Electricity",
    "Sanitation",
    "Health",
    "Education",
    "Other"
]

def categorize_issue_with_openai(issue_text):
    system_prompt = f"You are an assistant that categorizes civic problems into one of these categories: {', '.join(CATEGORIES)}. Only return the category name."
    user_prompt = f"Problem: {issue_text}\nCategory:"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=10,
            temperature=0
        )
        category = response.choices[0].message.content.strip()
        if category not in CATEGORIES:
            category = "Other"
        return category
    except Exception as e:
        st.warning(f"AI categorization failed: {e}. Defaulting to 'Other'.")
        return "Other"

# --- Issue Reporting Form ---
with st.form("issue_form"):
    st.subheader("Describe the Civic Issue")
    issue_text = st.text_area("Describe the issue in your local language *", max_chars=500)
    
    # Image upload
    image_file = st.file_uploader("Upload a photo of the issue (optional, max 5MB)", type=["jpg", "jpeg", "png"])
    image_caption = st.text_input("Optional: Add a caption for the image")

    # Voice upload
    audio_file = st.file_uploader("Upload a voice recording of the issue (optional, max 5MB)", type=["wav", "mp3", "m4a"])

    # Location input
    location_text = st.text_input("Enter your city or village *")
    st.caption("(Future: Pin-drop on map)")

    consent = st.checkbox("I agree to donate my data for open-source AI training (required)", value=False)
    submit = st.form_submit_button("Submit")

    # File size checks
    image_too_large = False
    audio_too_large = False
    if image_file is not None:
        image_file.seek(0, 2)
        if image_file.tell() > 5 * 1024 * 1024:
            image_too_large = True
        image_file.seek(0)
    if audio_file is not None:
        audio_file.seek(0, 2)
        if audio_file.tell() > 5 * 1024 * 1024:
            audio_too_large = True
        audio_file.seek(0)

    if submit:
        # Language detection if auto mode
        detected_lang = None
        if language_mode == "Auto-detect" and issue_text.strip():
            try:
                detected_lang = detect(issue_text)
            except LangDetectException:
                detected_lang = "Could not detect language."
        elif language_mode == "Manual":
            detected_lang = language_codes[language_names.index(selected_language)]
        else:
            detected_lang = None

        if not issue_text.strip():
            st.error("Please enter a description of the issue (required).")
        elif not consent:
            st.error("Consent is required to submit.")
        elif not location_text.strip():
            st.error("Please enter your city or village (required).")
        elif image_too_large:
            st.error("Image file is too large (max 5MB). Please upload a smaller file.")
        elif audio_too_large:
            st.error("Audio file is too large (max 5MB). Please upload a smaller file.")
        else:
            # Prepare file data
            image_bytes = image_file.read() if image_file is not None else None
            audio_bytes = audio_file.read() if audio_file is not None else None
            # Save to DB
            db.insert_submission(
                issue_text=issue_text,
                language=detected_lang,
                location=location_text,
                consent=consent,
                image=image_bytes,
                image_caption=image_caption,
                audio=audio_bytes,
                username=st.session_state['username']
            )
            st.success("Thank you for your submission! Your report has been saved.")
            st.write(f"**Language:** {detected_lang}")
            st.write(f"**Issue Description:** {issue_text}")
            st.write(f"**Location:** {location_text}")
            if image_file is not None:
                st.image(image_file, caption=image_caption or "Uploaded Image", use_column_width=True)
                st.write(f"**Image Caption:** {image_caption}")
            if audio_file is not None:
                st.audio(audio_file, format='audio/wav')
                st.write("**Voice recording uploaded.")
            st.info("(Data also saved to local database.)")
            # Reset form fields (Streamlit does not natively reset, so suggest refresh)
            st.info("You may refresh the page to submit another report.")

# --- Admin Dashboard ---
st.sidebar.markdown("---")
if st.session_state['username'].lower() == 'admin':
    show_dashboard = st.sidebar.checkbox("Show Admin Dashboard")
    if show_dashboard:
        st.header("Admin Dashboard: Submissions Preview & Stats")
        submissions = db.fetch_all_submissions()
        if not submissions:
            st.info("No submissions yet.")
        else:
            import pandas as pd
            import io, json
            df = pd.DataFrame([row[:10] for row in submissions], columns=["id", "issue_text", "language", "location", "consent", "image", "image_caption", "audio", "created_at", "username"])
            st.subheader("All Submissions")
            st.dataframe(df[["created_at", "username", "language", "location", "consent", "issue_text", "image_caption"]])
            # Export buttons (exclude image/audio blobs)
            export_cols = ["created_at", "username", "language", "location", "consent", "issue_text", "image_caption"]
            csv_buffer = io.StringIO()
            df[export_cols].to_csv(csv_buffer, index=False)
            st.download_button("Download CSV", csv_buffer.getvalue(), file_name="submissions.csv", mime="text/csv", key="csv_download")
            json_str = df[export_cols].to_json(orient="records", force_ascii=False)
            st.download_button("Download JSON", json_str, file_name="submissions.json", mime="application/json", key="json_download")
            # Language distribution chart
            lang_counts = df["language"].value_counts().reset_index()
            lang_counts.columns = ["Language", "Count"]
            fig = px.bar(lang_counts, x="Language", y="Count", title="Submissions by Language")
            st.plotly_chart(fig, use_container_width=True)
            # Preview images/audio for first 3 submissions
            st.subheader("Sample Media Preview (first 3)")
            for i, row in df.head(3).iterrows():
                st.markdown(f"**Submission {row['id']} ({row['created_at']}):**")
                if row["image"]:
                    st.image(row["image"], caption=row["image_caption"] or "Uploaded Image", use_column_width=True)
                if row["audio"]:
                    st.audio(row["audio"], format='audio/wav')
                st.write(f"**Text:** {row['issue_text']}")
                st.write(f"**Location:** {row['location']}")
                st.write("---")
            # Map visualization
            from geopy.geocoders import Nominatim
            import folium
            from streamlit_folium import st_folium
            st.subheader("Submission Locations Map")
            geolocator = Nominatim(user_agent="civicvoice-app")
            m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)  # Center on India
            mapped = 0
            unmapped = 0
            for loc, text in zip(df["location"], df["issue_text"]):
                try:
                    geo = geolocator.geocode(loc, timeout=5)
                    if geo:
                        folium.Marker([geo.latitude, geo.longitude], popup=text).add_to(m)
                        mapped += 1
                    else:
                        unmapped += 1
                except Exception:
                    unmapped += 1
            st_folium(m, width=700, height=400)
            if unmapped > 0:
                st.warning(f"{unmapped} locations could not be mapped.")
            # Placeholder for Folium map
            st.caption("(Future: Map visualization of locations)")

# --- Placeholder for future features ---
st.markdown("---")
st.caption("Future: Add image upload, voice upload, location, and dashboard features.") 