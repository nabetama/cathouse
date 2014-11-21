# coding: utf-8
"""
See: https://developer.github.com/webhooks/
"""


import simplejson as json


class Writer(object):
    """
    Classify a payload and write message to send hipchat.
    """

    def __init__(self, req, body):
        self.event = req.headers['X-GitHub-Event']
        self.data  = json.loads(body)

    def write(self, msg_type='text'):
        klass = globals().get(self.event)
        if not klass:
            raise ImportError(self.event)
        return klass.message(self.data)


class XGitHubEventBase(object):
    @classmethod
    def message(cls, data):
        pass


class commit_comment(XGitHubEventBase):
    "Any time a Commit is commented on."
    @classmethod
    def message(cls, data):
        pass



class create(XGitHubEventBase):
    "Any time a Branch or Tag is created."
    pass


class delete(XGitHubEventBase):
    "Any time a Branch or Tag is deleted."
    pass


class issue_comment(XGitHubEventBase):
    "Any time an Issue is commented on."
    pass


class issues(XGitHubEventBase):
    """
    Any time an Issue is assigned, unassigned, labeled, unlabeled, opened, closed, or reopened.
    """
    pass


class pull_request_review_comment(XGitHubEventBase):
    """
    Any time a Commit is commented on while inside a Pull Request review (the Files Changed tab).
    """
    pass


class pull_request(XGitHubEventBase):
    """
    Any time a Pull Request is assigned, unassigned, labeled, unlabeled, opened, closed, reopened,
    or synchronized (updated due to a new push in the branch that the pull request is tracking).
    """
    @classmethod
    def message(cls, data):
        return u'はろわ'


class push(XGitHubEventBase):
    """
    Any Git push to a Repository, including editing tags or branches. Commits via API actions that
    update references are also counted. This is the default event.
    """
    @classmethod
    def message(cls, data):
        s = '{commiter} pushed to <a href="{repos_url}">{repos}</a>.<br />' + \
            'Commit Log: {commit_message:<15}' + \
            '<a href="{commits_url}">Show diff.</a>'
        s = s.format(
                commiter        = data['pusher']['name'],
                repos_url       = data['repository']['html_url'],
                repos           = data['repository']['full_name'],
                commit_message  = data['head_commit']['message'].encode('utf-8'),
                commits_url     = data['head_commit']['url'],
                )
        return s

