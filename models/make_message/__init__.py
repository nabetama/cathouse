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
    AVATOR = '<img src="{}" width="30px" height="30px;"/>'
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
    @classmethod
    def message(cls, data):
        s = cls.AVATOR
        s += '{user} created {kind} on <a href="{repos_url}">{repos}</a>.<br />'
        msg = s.format(
                avator = data['sender']['avatar_url'],
                user = data['sender']['login'],
                kind = data['ref_type'],
                repos_url = data['repository']['html_url'],
                repos = data['repository']['full_name'],
                )
        return msg


class delete(XGitHubEventBase):
    "Any time a Branch or Tag is deleted."
    pass


class issue_comment(XGitHubEventBase):
    "Any time an Issue is commented on."
    @classmethod
    def message(cls, data):
        s = cls.AVATOR
        s += '{user} commented on <a href="{repos_url}">{repos}</a>.<br />' + \
            'Title: {issue_title}<br />' + \
            '<a href="{issue_url}">Show issue.</a>'
        msg = s.format(
                avator = data['sender']['avatar_url'],
                user = data['sender']['login'],
                repos_url = data['repository']['html_url'],
                repos = data['repository']['full_name'],
                issue_title = data['issue']['title'],
                issue_url = data['issue']['url'],
                )
        return msg


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
        s = cls.AVATOR
        s += '{commiter} pushed to <a href="{repos_url}">{repos}</a>.<br />' + \
            'Commit Log: {commit_message:<15}...<br />' + \
            '<a href="{commits_url}">Show diff.</a>'
        msg = s.format(
                avator          = data['sender']['avatar_url'],
                commiter        = data['pusher']['name'],
                repos_url       = data['repository']['html_url'],
                repos           = data['repository']['full_name'],
                commit_message  = data['head_commit']['message'].encode('utf-8'),
                commits_url     = data['head_commit']['url'],
                )
        return msg

