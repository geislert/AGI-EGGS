import smtplib
from email.mime.text import MIMEText
from pathlib import Path
from typing import List

from feedgen.feed import FeedGenerator


class NotificationService:
    """Create RSS feeds and send email notifications."""

    def __init__(self, rss_path: str, smtp_server: str = None, smtp_port: int = 25,
                 from_addr: str = None, to_addrs: List[str] | None = None):
        self.rss_path = Path(rss_path)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.from_addr = from_addr
        self.to_addrs = to_addrs or []
        self.feed = FeedGenerator()
        self.feed.title("AGI-EGGS Notifications")
        self.feed.link(href="http://localhost/")
        self.feed.description("Event notifications from AGI-EGGS")

    def add_event(self, title: str, content: str) -> None:
        """Append an event to the RSS feed and optionally email it."""
        entry = self.feed.add_entry()
        entry.title(title)
        entry.description(content)
        # send email if configured
        if self.smtp_server and self.from_addr and self.to_addrs:
            msg = MIMEText(content)
            msg["Subject"] = title
            msg["From"] = self.from_addr
            msg["To"] = ", ".join(self.to_addrs)
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as s:
                s.sendmail(self.from_addr, self.to_addrs, msg.as_string())

    def write_feed(self) -> None:
        """Write the RSS feed to disk."""
        self.feed.rss_file(self.rss_path)
