import sys
import os
from werkzeug.debug import DebuggedApplication

sys.path.insert(0, '/var/www/crocomi.re/')
import monitor

monitor.start(interval=1.0)
monitor.track(os.path.join(os.path.dirname(__file__), 'site.cf'))

from crocomire import app
#application = DebuggedApplication(app, True)
application = app
