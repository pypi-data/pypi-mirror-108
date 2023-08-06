from jira_tracker.logger import logger

class TrackerIssue:
    def __init__(self, jira_issue):
        self.data = jira_issue
    
    @property
    def name(self):
        return str(self.data)

    @property
    def summary(self):
        return str(self.data.fields.summary)

    @property
    def status(self):
        return str(self.data.fields.status)

    @property
    def points(self):
        return str(self.data.fields.customfield_10016)