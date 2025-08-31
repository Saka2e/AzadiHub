# AzadiHub

AzadiHub is an open-source project dedicated to providing free VPN configurations to promote internet freedom. It supports multiple protocols (VMess, VLESS, Trojan, Shadowsocks, SSR) and offers a user-friendly web interface to browse and copy configurations. The project uses a Django backend with a crawler to collect and update configurations regularly.

## Features
- **Dynamic Configs**: Automatically updated VPN configurations from various sources.
- **Protocol Filtering**: Filter configs by protocol (e.g., VMess, VLESS) via the web interface.
- **Responsive Design**: Built with Tailwind CSS and Font Awesome for a modern, mobile-friendly UI.
- **Donation Support**: Supports donations via Bitcoin, Ethereum, Tron, and Toncoin.
- **Roadmap & About**: Includes sections for project goals and future plans.

## Project Structure

```
.
├── api/                # REST API for accessing configurations
├── azadihub/          # Django project settings and URLs
├── crawler/           # Scripts for crawling and updating configs
├── static/            # Static files (CSS, JS, config files)
├── staticfiles/       # Collected static files for production
├── templates/         # HTML templates for the web app
├── web/               # Web app for the frontend
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Prerequisites
- Python 3.8+
- Django 4.x
- PostgreSQL or SQLite (default)
- Git
- Node.js (optional, for Tailwind CSS if using local build)

## Installation
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/RaitonRed/AzadiHub.git
    cd AzadiHub
    ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   ```bash
   python manage.py migrate
   ```

5. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000` in your browser.

## Usage
- **Home Page**: View the number of active configs and supported protocols.
- **Configs Page**: Browse and copy VPN configurations, filter by protocol.
- **Donation Page**: Support the project via cryptocurrency addresses.
- **Run Crawler**: Update configs using:
   ```bash
   python manage.py update_config
   ```

## Configuration
Edit `azadihub/settings.py` to customize:
- **Database**: Configure `DATABASES` for PostgreSQL or other databases.
- **Static Files**: Ensure `STATICFILES_DIRS` and `STATIC_ROOT` are set correctly.
- **Templates**: Templates are loaded from the `templates/` directory.

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a Pull Request.

## Roadmap
- **Phase 1**: Add support for HY2 and TUIC protocols by Q4 2025.
- **Phase 2**: Develop a mobile app for easy config access by Q1 2026.
- **Phase 3**: Build a community forum for users by Q4 2026.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.