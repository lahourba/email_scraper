# Newsletter Summarizer

## Description

This program retrieves newsletters from a specific label in your Gmail account, generates a clear and concise summary using the OpenAI GPT API, and sends the summary back to you via email in an HTML format.

### Key Features

1. **Automatic Email Retrieval**: Fetches emails from a specific Gmail label (e.g., "To Read").
2. **Smart Summarization**: Generates summaries of newsletters using the OpenAI GPT API.
3. **HTML Formatting**: Produces well-structured and visually appealing summaries.
4. **Automated Email Sending**: Sends the summary via email to a predefined recipient.

---

## Prerequisites

### Required Tools and Libraries

1. **Python** (>= 3.7)
2. **Python Libraries**:
   - `openai`
   - `google-auth`
   - `google-auth-oauthlib`
   - `google-auth-httplib2`
   - `google-api-python-client`
   - `re` (standard)
3. **Gmail Account**:
   - API access enabled for Gmail.
   - OAuth 2.0 credentials file (`credentials.json`) created in the Google Cloud Console.
4. **OpenAI API Key**:
   - A valid OpenAI API key (set as an environment variable: `OPENAI_API_KEY`).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lahourba/newsletter_summarizer.git
   cd email_scraper
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Gmail OAuth Credentials**:
   - Place your `credentials.json` file in the project root directory.

5. **Set Up OpenAI API Key**:
   - Add your API key as an environment variable:
     ```bash
     export OPENAI_API_KEY="your_openai_api_key"
     ```

---

## Configuration

### Adjusting Parameters

1. **Gmail Label**: Ensure newsletters are placed under a specific label (e.g., "To Read"). Update this label in the main script (`main.py`) if needed:

   ```python
   emails = get_emails_from_label(service, label_name="To Read", max_results=20)
   ```

2. **Recipient Email Address**: Set the recipient email address in the main script (`main.py`):

   ```python
   to_email="your_email@example.com"
   ```

---

## Usage

### Running the Program

1. Delete old tokens if necessary:
   ```bash
   rm token.json
   ```

2. Execute the main script:
   ```bash
   python main.py
   ```

   The program will:
   - Authenticate via Gmail API.
   - Fetch emails from the specified label.
   - Generate summaries using GPT.
   - Format the summary in HTML.
   - Send the summary via email.

---

## Project Structure

```
newsletter-summarizer/
├── gmail_auth.py          # Handles Gmail OAuth authentication
├── read_emails.py         # Fetches emails from a Gmail label
├── main.py                # Orchestrates the entire process
├── requirements.txt       # Lists Python dependencies
├── credentials.json       # OAuth credentials for Gmail (not versioned)
├── token.json             # OAuth token generated automatically
```

---

## Detailed Workflow

1. **Gmail Authentication**:
   - `gmail_auth.py` handles OAuth 2.0 authentication for accessing the Gmail API.
   - A `token.json` file is generated to remember the access.

2. **Email Retrieval**:
   - Emails from the specified label are retrieved using `read_emails.py`.

3. **Email Summarization**:
   - Each newsletter is summarized via the OpenAI GPT API using `openai.chat.completions.create`.
   - Bullet points are converted to structured HTML `<ul>` lists, and bold text is wrapped in `<strong>` tags.

4. **Email Sending**:
   - The HTML summary is sent to the recipient using the Gmail API.

---

## Automation

To automate the script (e.g., every Monday morning), use a scheduler.

### On Linux/macOS: Crontab

Add a task using `crontab -e`:

```bash
0 9 * * 1 /path/to/venv/bin/python /path/to/main.py
```

### On Windows: Task Scheduler

- Create a new task.
- Configure it to run the script using `python` in the virtual environment.

---

## Contributions

Contributions are welcome! If you have suggestions or encounter bugs, feel free to open an issue or submit a pull request.

---

## Author

- **Sébastien Albou**  
  Creator of the program.  
  [Contact Me](mailto:seb.albou@datafed.fr)


