import os, math

filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'highscores.save')
maxPoints = 999999
scoreBytes = math.ceil(math.log2(maxPoints)/8)

nameLength = 20
nameBytes = 2*(1+nameLength)

def loadFile():
    scores = ScoreList()
    with open(filepath, 'rb') as file:
        while file.readable():
            data = file.read(scoreBytes+nameBytes)
            if len(data) > 0:
                points = int.from_bytes(data[:3], 'big')
                name = data[5:].decode('utf-16')
                scores.addScore(Score(str(name).replace('\n', ''), points))
            else:
                break
    file.closed
    return scores

def saveFile(scores):
    with open(filepath, 'wb') as file:
        for score in iter(scores):
            file.write(int(score.points).to_bytes(scoreBytes, 'big'))
            file.write(str(score.name + (nameLength-len(score.name))*'\n').encode('utf-16'))
    file.closed



class ScoreList:
    def __init__(self):
        self.scores = []
    def __iter__(self):
        self.i = 0
        return self
    def __next__(self):
        if self.i < len(self.scores):
            self.oldI = self.i
            self.i += 1
            return self.scores[self.oldI]
        else:
            raise StopIteration
    def addScore(self, score):
        self.scores.append(score)
        self.sortScores()
        if len(self.scores) > 10:
            self.scores = self.scores[:10]
    def removeScore(self, score):
        self.scores.remove(score)
    def clear(self):
        self.scores.clear()
    def sortScores(self):
        self.scores = sorted(self.scores, key=lambda score: score.points, reverse=True)
    def checkScore(self, score):
        if len(self.scores) < 10:
            return True
        else:
            for savedScore in self.scores:
                if score > savedScore.points:
                    return True
            return False

class Score:
    def __init__(self, name, points):
        self.name = name
        self.points = points