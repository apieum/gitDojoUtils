import sys
import os
import unittest
from gitDojoUtils.hooks.commitMsg import RefactoringMsg


class RefactoringMsgTest(unittest.TestCase):
    messageFile = os.path.realpath('_commitMsg')
    commitMessage = '@user1 move method, @user2 move method and move field'

    @classmethod
    def setUpClass(cls):
        message = open(cls.messageFile, 'w')
        message.write(cls.commitMessage)
        message.close()
        exitWithError = lambda obj: "exit with error"
        exitNormally = lambda obj: "exit normally"
        setattr(RefactoringMsg, 'exitWithError', exitWithError)
        setattr(RefactoringMsg, 'exitNormally', exitNormally)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.messageFile)

    def setUp(self):
        config = {
            'hook': 'RefactoringMsg',
            'keywords': ['move method', 'move field'],
            'score': os.path.join(os.path.dirname(__file__), 'score.txt')
        }
        sys.argv = ['gitCommit', self.messageFile]
        self.hook = RefactoringMsg(config)

    def tearDown(self):
        os.remove(os.path.join(os.path.dirname(__file__), 'score.txt'))

    def test_commitMsg_open_arg1_to_read_commit_message(self):
        self.assertEquals(self.commitMessage, self.hook.message)

    def test_it_split_message_by_users(self):
        expected = {
            '@user1': 'move method,',
            '@user2': 'move field'
        }

        inlineMsg = ''
        for user, msg in expected.items():
            inlineMsg += '%s %s ' % (user, msg)

        self.assertEquals(expected, self.hook.splitUsersMsg(inlineMsg.strip(), self._returnAsIs))

    def test_it_transform_user_message_in_a_list_of_matches_given_by_config(self):
        expected = {
            '@user1': 2,
            '@user2': 1
        }
        inlineMsg = '@user1: move method and move field, @user2 move field only'
        self.assertEquals(expected, self.hook.countPoints(inlineMsg, self.hook.commitScore))

    def test_it_counts_users_points_depending_on_matches(self):
        expected = ['move method', 'move field', 'move field']
        userMessage = 'dqsfkj ' + expected[0] + ' move ' + expected[1] + ' field ' + expected[2]
        self.assertEquals(expected, self.hook.listKeywords(userMessage))

    def _returnAsIs(self, userAction):
        return userAction
