


class FigshareArticle(object):


    def __init__(self, aid, location):
        self._aid = aid
        self._location = location
        self._files = []


    def add_file(self, fig_file):
        self._files.append(fig_file)


    @property
    def files(self):
        return  self._files


    @property
    def aid(self):
        return  self._aid


    @property
    def location(self):
        return  self._location



class FigshareFile(object):


    def __init__(self, fid, location):
        self._fid = fid
        self._location = location


    @property
    def fid(self):
        return  self._fid


    @property
    def location(self):
        return  self._location


