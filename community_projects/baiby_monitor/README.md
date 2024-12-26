
# BAIby Monitor

The BAIby Monitor project is an open-source initiative aimed at developing a smart baby monitoring system that utilizes machine learning to detect a baby's cries and other activities, providing real-time notifications to parents or caregivers.

## Features

- **Cry Detection**: Employs machine learning algorithms to distinguish a baby's cries from other sounds, ensuring accurate alerts.
- **Real-Time Notifications**: Sends immediate alerts to connected devices when the baby cries or unusual activity is detected.
- **Activity Monitoring**: Tracks the baby's movements and sounds, offering insights into sleep patterns and behavior.
- **User-Friendly Interface**: Provides an intuitive dashboard for monitoring and configuring settings.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/shlomi1993/hailo-CLIP.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd hailo-CLIP/community_projects/baiby_monitor
   ```

3. **Install Dependencies**:

   Ensure you have [Python 3.8](https://www.python.org/downloads/release/python-380/) or higher installed. Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Environment**:

   Create a `.env` file in the project directory and add necessary configuration variables as specified in `.env.example`.
   
   ** Telegram Bot Activation **:
   a. Find @bAIbyMonbot in the 'Telegram' App.
   b. Press the 'Start' Button.
   c. You are ready to receive messages to your Telegram.

6. **Run the Application**:

   ```bash
   python main.py
   ```

## Usage

- **Access the Dashboard**: Once the application is running, navigate to `http://localhost:8000` in your web browser to access the monitoring dashboard.
- **Configure Settings**: Use the dashboard to adjust sensitivity levels, notification preferences, and other settings.
- **Monitor Alerts**: Receive real-time notifications on the dashboard and connected devices when the system detects the baby crying or unusual activity.

## Demo Video

For a visual demonstration of the BAIby Monitor project, watch this video:
[BAIby Monitor Demo](https://youtu.be/sXgL5g_A-u0)

## Contributing

We welcome contributions from the community! To contribute:

1. **Fork the Repository**: Click the 'Fork' button on the top right of the repository page.
2. **Create a New Branch**: Use `git checkout -b feature-branch-name` to create a branch for your feature or bug fix.
3. **Make Changes**: Implement your feature or fix. Ensure your code follows the project's coding standards.
4. **Commit Changes**: Use `git commit -m "Description of your changes"` to commit your modifications.
5. **Push to GitHub**: Use `git push origin feature-branch-name` to push your changes.
6. **Create a Pull Request**: Navigate to your forked repository on GitHub and click the 'New Pull Request' button.

Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for detailed guidelines.
