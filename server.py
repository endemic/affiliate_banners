import cherrypy
import sqlite3
import json
import random

DATABASE = 'database.sqlite'

def setup_db():
    if (ENV is 'production'):
        self.DATABASE = 'production.sqlite'
    else:
        self.DATABASE = 'test.sqlite'

    with sqlite3.connect(DATABASE) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS "units" (
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "imgsrc" TEXT NOT NULL,
            "description" TEXT NOT NULL,
            "url" TEXT NOT NULL,
            "weight" REAL NOT NULL DEFAULT 1.0,
            "clicks" INTEGER NOT NULL DEFAULT 0,
            "active" INTEGER NOT NULL DEFAULT 0
        );''')



    # Put in a few test entries
    #c.execute('''INSERT INTO "units" ("imgsrc", "description", "url", "weight", "active")
    #                          VALUES ("https://nathandemick.com/assets/images/nonogram-madness.png", "Testing, yo!", "https://ganbarugames.com", 0.5, 1);''')
    #c.execute('''INSERT INTO "units" ("imgsrc", "description", "url", "weight", "active")
    #                          VALUES ("https://nathandemick.com/assets/images/nonogram-madness.png", "Testing 2, yo!", "https://ganbarugames.com", 0.25, 1);''')
    #c.execute('''INSERT INTO "units" ("imgsrc", "description", "url", "weight", "active")
    #                          VALUES ("https://nathandemick.com/assets/images/nonogram-madness.png", "Testing 3, yo!", "https://ganbarugames.com", 0.75, 1);''')
    #c.execute('''INSERT INTO "units" ("imgsrc", "description", "url", "weight", "active")
    #                          VALUES ("https://nathandemick.com/assets/images/nonogram-madness.png", "Should never see this", "https://ganbarugames.com", 1.0, 0);''')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class WebApp(object):
    def __init__(self):
        setup_db()

    def _cp_dispatch(self, vpath):
        # /follow/:id
        if (vpath[0] is 'follow' and isinstance(vpath[1], int)):
            cherrypy.request.params['id'] = vpath.pop()
            return self.follow

        return vpath

    @cherrypy.expose
    def follow(self, id):
        id = int(id)

        with sqlite3.connect(DATABASE) as c:
            c.row_factory = dict_factory
            # Update # of clicks
            c.execute('UPDATE units SET clicks = clicks + 1 WHERE id = ?', (id,))
            c.commit() # is this necessary?

            # Get redirect URL
            query = c.execute('SELECT * FROM units WHERE id = ?', (id,))
            result = query.fetchone()
            raise cherrypy.HTTPRedirect(result['url'])

    @cherrypy.expose
    def index(self):
        with sqlite3.connect(DATABASE) as c:
            c.row_factory = dict_factory
            query = c.execute('SELECT * FROM units WHERE active = 1 ORDER BY RANDOM()')
            rows = query.fetchall()

            result = None
            while result is None:
                for row in rows:
                    if row['weight'] > random.random():
                        result = row
                        break

            return json.dumps(result)

if __name__ == '__main__':
    cherrypy.quickstart(WebApp(), '/')
