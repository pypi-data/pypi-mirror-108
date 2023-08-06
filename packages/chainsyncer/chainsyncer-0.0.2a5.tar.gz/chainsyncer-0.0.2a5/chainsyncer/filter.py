# standard imports
import logging

# local imports
from .error import BackendError

logg = logging.getLogger(__name__)


class SyncFilter:

    def __init__(self, backend):
        self.filters = []
        self.backend = backend


    def add(self, fltr):
        if getattr(fltr, 'filter') == None:
            raise ValueError('filter object must implement have method filter')
        logg.debug('added filter "{}"'.format(str(fltr)))

        self.filters.append(fltr)
   

    def apply(self, conn, block, tx):
        session = None
        try:
            session = self.backend.connect()
        except TimeoutError as e:
            self.backend.disconnect()
            raise BackendError('database connection fail: {}'.format(e))
        i = 0
        (pair, flags) = self.backend.get()
        for f in self.filters:
            if not self.backend.check_filter(i, flags):
            #if flags & (1 << i) == 0:
                logg.debug('applying filter {} {}'.format(str(f), flags))
                f.filter(conn, block, tx, session)
                self.backend.complete_filter(i)
            else:
                logg.debug('skipping previously applied filter {} {}'.format(str(f), flags))
            i += 1

        self.backend.disconnect()

class NoopFilter:
    
    def filter(self, conn, block, tx, db_session=None):
        logg.debug('noop filter :received\n{} {} {}'.format(block, tx, id(db_session)))


    def __str__(self):
        return 'noopfilter'
