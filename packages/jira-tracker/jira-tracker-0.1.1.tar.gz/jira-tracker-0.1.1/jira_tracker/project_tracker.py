from jira_tracker.logger import logger
from jira_tracker.tracker_issue import TrackerIssue
import datetime

class ProjectTracker:
    def __init__(self, jira_client, project_key):
        self.jira = jira_client
        self.key = project_key
    
    def this_weeks_issues(self):
        result = self.jira.search_issues(
            f"project = {self.key} AND assignee = currentuser() AND ((resolutiondate >= -{datetime.datetime.today().weekday()}d AND status = Done) OR status != Done)"
        )
        logger.debug(f"Found {len(result)} valid records this week in {self.key}")

        issues = []
        for issue in result:
            issues.append(TrackerIssue(issue))

        return issues