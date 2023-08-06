import argparse, traceback, sys
from jira_tracker.logger import logger, enable_debug_logger
from jira_tracker.jira_auth import JiraAuth
from jira_tracker.project_tracker import ProjectTracker

version = "0.1.1"

def main():
    
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("-d", "--debug", help="Enables debug logging and traceback", action="store_true", dest="debug", default=False)
    parser.add_argument("-v", "--version", help="Return current version number", dest="return_version", action="store_true", default=False)
    parser.add_argument("--update-config", help ="Prompts input for updating config file", dest="update_config", action="store_true", default=False)

    args = parser.parse_args()

    try:
        if args.debug:
            enable_debug_logger()

        if args.return_version:
            print(version)
            return


        auth = JiraAuth()

        if args.update_config:
            auth.stdin_configure()
            auth.update_config(auth.config_location)

        
        row_format ="{:<12}{:<64}{:>4}{:>16}"
        print(row_format.format("Task","Summary","Points","Status"))

        points = 0
        jira_client = auth.get_client()
        all_issues = []
        for jira_project in jira_client.projects():
            logger.debug(f"Searching Project: {jira_project.key}")
            proj = ProjectTracker(jira_client, jira_project.key)
            issues = sorted(proj.this_weeks_issues(), key=lambda issue: issue.status)
            all_issues = all_issues + issues
            for issue in issues:
                if issue.status == "Done":
                    points = points + float(issue.points)

        for issue in all_issues:
            print(row_format.format(issue.name, issue.summary, issue.points, issue.status))
        print(f"\nTotal points this week: {points}")


    except (Exception) as e:
        logger.critical(e)
        if args.debug:
            tb = sys.exc_info()[2]
            traceback.print_tb(tb)


if __name__ == '__main__':
    main()