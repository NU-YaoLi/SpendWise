Hackathon Project Proposal: SpendWise
Team Name: AI Told You So
Members: Yao Li, Shuxin Yang, Kemmei Nakamoto, Wuyin Kang, Siyi Pan

1. Problem Statement
Many people struggle with tracking their daily expenses, leading to poor budgeting and financial management. Manually entering expenses is time-consuming, and basic OCR tools often fail to recognize receipts correctly. 
SpendWise, an AI-Powered Expense Tracker, solves this by using AI-powered OCR and NLP to extract and categorize expenses automatically, making personal finance tracking effortless for users.

2. Proposed Solution
SpendWise is an AI-driven receipt scanner that extracts store names, total cost, tax, and itemized details from receipts. 
It automatically categorizes expenses (food, transport, shopping) and provides monthly spending insights to help users manage their budgets effectively.

Key features will be:
•	AI-Powered Receipt Scanning: Extracts text from receipts with high accuracy.
•	Automatic Expense Categorization: AI learns spending patterns and assigns correct labels.
•	Spending Insights & Budgeting Tips: Tracks monthly expenses and provides useful financial suggestions.
•	Simple & Lightweight UI: Designed for fast and easy receipt uploads.

3. Impact on Users
Who:
•	Students – Need an easy way to track expenses without manual input.
•	Freelancers & Young Professionals – Want a quick solution for organizing receipts.
•	Anyone Managing a Budget – Looking for AI-driven spending insights.
How:
•	Reduces financial stress by automating expense tracking.
•	Improves budgeting skills with clear spending insights.
•	Saves time by eliminating manual data entry.

4. Technical Stack
•	Languages: Python (Backend AI), JavaScript (React), Dart (Flutter)
•	Frameworks & APIs: Tesseract OCR, Google Vision API, OpenAI GPT
•	Database: PostgreSQL (on-premises) for secure local data storage
•	Deployment: Snapdragon Windows laptop (no cloud dependency)
•	Version Control: GitHub for collaboration

5. Challenges & Mitigation Methods
Challenge	Solution
AI may mis-categorize expenses	Allow manual correction to improve AI learning
Users may forget to upload receipts	Implement a notification/reminder system
UI complexity may discourage adoption	Keep the interface minimal and intuitive

6. Budget
Item	Estimated Cost
API Costs (OCR, GPT)	Unknown
Development Tools	$0 (Open-source)
Hosting & Domain	$0 (Local)
Hardware (Laptop)	Existing Snapdragon Windows device

7. Project Timeline
Phase	Tasks	Duration
March 1-2	Research OCR & AI models, set up repo	2 days
March 3-5	Develop OCR pipeline	3 days
March 6-8	Implement AI categorization	3 days
March 9-11	Build UI and receipt upload feature	3 days
March 12-13	Develop spending insights module	2 days
March 14-15	Testing, bug fixes, final refinements	2 days

8. Demo & Presentation Plan
•	Live Demo: Show how SpendWise scans and categorizes receipts.
•	Comparison: Before-and-after results of manual vs AI-driven tracking.
•	User Feedback: Showcase ease of use and impact on budgeting.

9. Future Improvements
•	Smart Store Recommendations: to help users find the most cost-effective supermarkets and stores based on spending history.
