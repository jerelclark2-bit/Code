import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])

class PortfolioChecks(unittest.TestCase):
    def test_site_links_and_sections(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        p = PageParser()
        p.feed(text)
        self.assertIn("projects", p.ids)
        self.assertIn("about", p.ids)
        for link in p.links:
            if link.startswith("#"):
                self.assertIn(link[1:], p.ids)
            elif not link.startswith("https://") and link != "./":
                self.assertTrue((ROOT / link).exists(), link)

    def test_profile_draft_exists(self):
        s = (ROOT / "PROFILE_README.md").read_text(encoding="utf-8")
        for project in ("BarnacleAI", "GREENLIGHT", "NeuroFridge"):
            self.assertIn(project, s)

if __name__ == "__main__":
    unittest.main()
