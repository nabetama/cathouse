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
    AVATAR = '<img src="{avatar}" width="30px" height="30px;"/>'
    @classmethod
    def message(cls, data):
        return cls.AVATAR.format(
                avatar = data['sender']['avatar_url'],
                )


class commit_comment(XGitHubEventBase):
    "Any time a Commit is commented on."
    @classmethod
    def message(cls, data):
        s = super(cls, cls()).message(data)
        s += '{user} commented <a href="{comit_url}">{repos}</a>.<br />' +\
             'Comment: {comment}...' +\
             ''
        msg = s.format(
                user      = data['sender']['login'],
                comit_url = data['comment']['html_url'],
                repos     = data['repository']['full_name'],
                comment   = data['comment']['body'].encode('utf-8'),
                )
        return msg


class create(XGitHubEventBase):
    "Any time a Branch or Tag is created."
    @classmethod
    def message(cls, data):
        s = super(cls, cls()).message(data)
        s += '{user} created {kind} on <a href="{repos_url}">{repos}</a>.<br />'
        msg = s.format(
                avatar    = data['sender']['avatar_url'],
                user      = data['sender']['login'],
                kind      = data['ref_type'],
                repos_url = data['repository']['html_url'],
                repos     = data['repository']['full_name'],
                )
        return msg


class delete(XGitHubEventBase):
    "Any time a Branch or Tag is deleted."
    @classmethod
    def message(cls, data):
        s = super(cls, cls()).message(data)
        s += 'Deleted {kind}({ref}) at <a href="{link}">{repos}</a>'
        msg = s.format(
                avatar = data['sender']['avatar_url'],
                kind   = data['ref_type'],
                ref    = data['ref'],
                link   = data['repository']['html_url'],
                repos  = data['repository']['full_name'],
                )
        return msg


class delete_branch(XGitHubEventBase):
    "Deleted branch"

    @classmethod
    def message(cls, data):
        s = super(cls, cls()).message(data)
        s += 'Deleted branch {kind} at <a href="{link}">{repos}</a>'
        msg = s.format(
                avatar = data["sender"]["avatar_url"],
                kind   = data["ref"],
                link   = data['repository']['html_url'],
                repos  = data['repository']['full_name'],
                )
        return msg


class issue_comment(XGitHubEventBase):
    "Any time an Issue is commented on."
    @classmethod
    def message(cls, data):
        s = super(cls, cls()).message(data)
        s += '{user} commented on <a href="{repos_url}">{repos}</a>.<br />' + \
            'Title: {issue_title}<br />' + \
            '<a href="{issue_url}">Show issue.</a>'
        msg = s.format(
                avatar      = data['sender']['avatar_url'],
                user        = data['sender']['login'],
                repos_url   = data['repository']['html_url'],
                repos       = data['repository']['full_name'],
                issue_title = data['issue']['title'],
                issue_url   = data['issue']['url'],
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
        if data.get("deleted"):
            return delete_branch.message(data)
        s = cls.AVATAR
        s += '{commiter} pushed to {ref} in <a href="{repos_url}">{repos}</a>.<br />' + \
            'Commit Log: {commit_message:<15}...<br />' + \
            '<a href="{commits_url}">Show diff.</a>'
        msg = s.format(
                avatar          = data['sender']['avatar_url'],
                ref             = data['ref'],
                commiter        = data['pusher']['name'],
                repos_url       = data['repository']['html_url'],
                repos           = data['repository']['full_name'],
                commit_message  = data['head_commit']['message'].encode('utf-8'),
                commits_url     = data['head_commit']['url'],
                )
        return msg

