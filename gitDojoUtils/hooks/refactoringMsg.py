import sys
import os
import re


class RefactoringMsg(object):
    def __init__(self, config={}):
        self.config = config
        self._validateArgs()
        self._initCommitMessage()
        score = self.countPoints(self.message, self.commitScore)
        self.writeScore(score)

    def commitScore(self, user, points):
        print "%s made %s points" % (user, points)

    def writeScore(self, score):
        oldScore = {}
        if os.path.exists(self.config['score']):
            scoreFile = open(self.config['score'], 'r')
            oldScore = self._extractScore(scoreFile.read())
            scoreFile.close()

        for user, points in score.items():
            if user not in oldScore:
                oldScore[user] = 0
            oldScore[user] += points

        scoreFile = open(self.config['score'], 'w')
        scoreFile.write(self._compactScore(oldScore))
        scoreFile.close()

    def _extractScore(self, scoreText):
        score = {}
        for userScore in scoreText.splitlines():
            userScore = userScore.split(':')
            score[userScore[0]] = int(userScore[1])
        return score

    def _compactScore(self, score):
        scoreText = ''
        for user, points in score.items():
            scoreText += "%s:%s\n" % (user, points)
        return scoreText

    def countPoints(self, message, showScore):
        usersKeywords = self.splitUsersMsg(message, self.listKeywords)
        usersScores = {}
        for user, keywords in usersKeywords.items():
            usersScores[user] = len(keywords)
            showScore(user, usersScores[user])
        return usersScores

    def splitUsersMsg(self, message, transform):
        usersPart = message.split('@')
        usersMsg = {}
        for userPart in usersPart[1:]:
            result = re.search('([a-z0-9]+)[\s:]+(.+)', userPart)
            user = '@%s' % result.group(1).strip()
            usersMsg[user] = transform(result.group(2).strip())
        return usersMsg

    def listKeywords(self, userMessage):
        pattern = []
        for keyword in self.config['keywords']:
            pattern.append(re.escape(keyword))
        pattern = re.compile('(' + '|'.join(pattern) + ')', re.IGNORECASE)
        return pattern.findall(userMessage)

    def exitWithError(self):
        sys.exit(1)

    def exitNormally(self):
        sys.exit(0)

    def _validateArgs(self):
        if len(sys.argv) < 2:
            self.exitWithError()

    def _initCommitMessage(self):
        commitFile = open(sys.argv[1])
        self.message = commitFile.read()
        commitFile.close()
