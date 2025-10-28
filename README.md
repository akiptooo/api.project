# Judiciary Information System - Case Management

The Judiciary Information System (JIS) is a Django-based web application designed to streamline and digitize court case management processes. The system provides an intuitive platform for managing case records, hearing schedules, judges’ assignments, and overall workflow within judicial institutions. By integrating Django’s robust backend with a clean Bootstrap-powered interface, the project aims to enhance transparency, accessibility, and efficiency in case handling and documentation.

This application is structured into multiple Django apps, each representing a specific module of the judiciary workflow. The Cases app handles the registration and tracking of court cases, storing details such as case numbers, parties involved, and statuses. The Hearings app manages court session dates and progress updates, while the Judges app maintains information about judicial officers and their case assignments. An optional Users app manages authentication, ensuring that only authorized staff—such as clerks, judges, and administrators—can access and update records. Each module interacts through Django’s ORM, providing secure and efficient database operations.

The frontend interface is developed using **Bootstrap 5** for a responsive and professional design, featuring dashboards, modals, and data tables for interactive management. Users can easily view case details, add new cases through a modal form, and update hearing information. Collaboration and version control are managed GitHub, with each team member contributing through feature branches and pull requests to maintain a clean code

To run the project locally, clone the repository and set up a virtual environment:
```bash
git clone https://github.com/your-group/judiciary-info-system.git
cd judiciary-info-system
python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
