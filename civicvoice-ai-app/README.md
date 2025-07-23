# CivicVoice: AI-Powered Public Service Feedback & Corpus Collection App

---

## 1.1 Team Information

- **Project Name**: CivicVoice – Public Feedback + Indic Corpus Engine
- **Team Members**:
  - Shivaganesh Mummadi (Team Lead & PM)
  - manishmiryanam13
  - udayraj1314
  - Prasanna 6111
  - Dhanush0602

- **Organization**: Swecha Internship Cohort 2025
- **Git Repo**: 
- **Live App**:

---

## 1.2 Application Overview (MVP Scope)

**Problem**: In Indian cities, civic issues like potholes, water leakage, and garbage piles remain unresolved due to poor reporting systems. Citizens have no easy way to report, and governments lack structured, multilingual data.

**Solution**: CivicVoice is a multilingual, offline-first, Streamlit app that allows users to report public issues using text, voice, image, and location. In the background, it collects rich, annotated, geo-tagged Indic language data for building open-source corpora.

### 💡 MVP Scope (Built in Week 1):
- Multilingual issue reporting (text, image, voice, GPS)
- Language auto-detection & STT transcription
- AI-powered classification and translation
- Admin dashboard with maps and analytics
- Data export in CSV/JSON
- Deployed on Hugging Face Spaces

---

## 1.3 AI Integration Details

| AI Function              | Model Used                     |
|--------------------------|--------------------------------|
| Speech-to-Text (STT)     | Whisper by OpenAI (base)       |
| Language Detection       | `langdetect` (lightweight)     |
| Text Classification      | Hugging Face BERT model fine-tuned for civic labels |
| Translation              | IndicTrans2 / NLLB             |

All AI results (label, language tag, translation) are saved alongside user data for research purposes.

---

## 1.4 Technical Architecture & Development

| Layer      | Tools Used                                 |
|------------|--------------------------------------------|
| Frontend   | Streamlit (for both users & admins)        |
| Backend    | Python scripts (utils, STT, classification)|
| Database   | PostgreSQL (locally), Firebase (media)     |
| AI Models  | Hugging Face, Whisper, IndicTrans2         |
| Maps       | Folium                                     |
| Charts     | Plotly                                     |
| Storage    | Firebase / AWS S3                          |
| Deployment | Hugging Face Spaces                        |

### Architecture Flow:
     ┌────────────────────────────┐
     │     Citizen User (UI)      │
     └────────────┬───────────────┘
                  │
       [Multilingual Streamlit App]
                  │
     ┌────────────▼────────────┐
     │  User Submits Form:     │
     │  - Text                 │
     │  - Voice (Optional)     │
     │  - Image (Optional)     │
     │  - Location (GPS/manual)│
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │      Preprocessing      │
     │ - Language Detection    │
     │ - STT (Whisper/Vosk)    │
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │    AI Processing Layer   │
     │ - Text Classification    │ ◄────── Uses Hugging Face BERT
     │ - Translation to English │ ◄────── Uses IndicTrans2 / NLLB
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │     Data Storage Layer  │
     │ - PostgreSQL (structured)│
     │ - Firebase/S3 (media)    │
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │     Admin Dashboard     │
     │ - Folium (Live Map)     │
     │ - Plotly (Issue Stats)  │
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │   Corpus Export Engine  │
     │ - text_corpus.csv       │
     │ - translations.csv      │
     │ - audio_data.json       │
     │ - image_meta.csv        │
     └─────────────────────────┘

---

## 1.5 User Testing & Feedback (Week 2)

### ✅ Methodology:
- Testers: 20 users from colleges and WhatsApp civic groups.
- Languages tested: English, Hindi, Tamil, Telugu.
- Devices: Low-end Android phones + spotty internet.

### ✅ Tasks Given:
- Submit 3 reports using different inputs (text + voice + image)
- Try with and without GPS
- Translate their own report
- Give feedback on loading time, layout, language issues

### 📝 Insights:
- Users loved voice input but wanted manual correction.
- GPS wasn’t always reliable in low-connectivity areas.
- Many users wanted their local dialect added.

### 🔧 Fixes Implemented:
- Manual location fallback
- UI tweaks for RTL languages
- Improved Whisper fallback with shorter timeouts

---

## 1.6 Project Lifecycle & Roadmap

### 🗓️ A. Week 1: Rapid Development Sprint

| Day | Task                                                      |
|-----|-----------------------------------------------------------|
| 1   | Set up repo, initial design, MVP wireframes               |
| 2   | Streamlit frontend (citizen form), Firebase setup         |
| 3   | Whisper STT + language detection integration              |
| 4   | Hugging Face civic issue classifier added                 |
| 5   | IndicTrans2 + location tagging                            |
| 6   | Admin dashboard (Plotly, Folium)                          |
| 7   | Full deployment on Hugging Face + corpus export scripts   |

**✅ Key Deliverables**:
- Functional MVP
- Offline-first UX
- AI-pipeline working end-to-end

---

### 🧪 B. Week 2: Beta Testing & Iteration Cycle

| Activity              | Description                                        |
|-----------------------|----------------------------------------------------|
| Recruit Testers       | Civic groups, students from Telangana & Tamil Nadu|
| Feedback Collection   | Google Forms + in-app rating                       |
| Iteration             | Added language manual override, simplified UI     |
| Low Bandwidth Fixes   | Reduced image size, added offline form version    |

---

### 📢 C. Weeks 3–4: User Acquisition & Corpus Growth

#### 🎯 Target Audience:
- College students in Tier-2 cities
- Village elders (for voice/dialect)
- Civic activists on WhatsApp
- Local language media outlets

#### 📈 Growth Strategy:
- “Contribute to Save Your City” Campaign
- College contests: Top 5 contributors win certificate
- Regional YouTube explainers
- CivicVoice Stickers shared on WhatsApp

#### 📊 Execution Summary:

| Metric                     | Result                         |
|----------------------------|--------------------------------|
| Unique Users               | 180+                           |
| Corpus Contributions       | 700+ reports in 9 languages    |
| Voice Reports              | 120+ (mostly Hindi + Telugu)   |
| Translations Verified      | 300+                           |
| Most Active Region         | Telangana & Tamil Nadu         |

---

## 🔮 D. Post-Internship Vision & Sustainability

### ✨ Major Future Features
- WhatsApp chatbot integration
- Admin ticket escalation system
- Dialect tagging (e.g., Awadhi, Dakhini)

### 👥 Community Building
- Build a Discord server
- Run “Language of the Week” events
- Corpus contributor leaderboard

### 📡 Scaling Data Collection
- More field partners (NGOs, Gram panchayats)
- Add camera-based OCR for handwritten complaints
- Auto-summarization of complaints

### 💡 Sustainability
- License data under Creative Commons
- Public access via Hugging Face Dataset repo
- Apply for research grants (Bhashini, MeitY, AI4Bharat)

---

### 🔗 Links

---

**Building with ❤️ by Team CivicVoice | Swecha Open-Source Internship 2025**


## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://code.swecha.org/shivaganeshmummadi/civicvoice-ai-app.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://code.swecha.org/shivaganeshmummadi/civicvoice-ai-app/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
