'''A custom Django administrative command for promoting data.

This command removes the existing data in the PublicTraitData table and
replaces it with the most recent data from the "development" TraitData
table.

'''

import datetime

from django.core.management.base import BaseCommand
from django.db import connection, transaction

from primcom.models import PublicTraitData


class Command(BaseCommand):
    '''A custom command to promote data.'''

    help = 'Promotes development data to the public site.'
    args = ''

    def _promote_devel(self):
        '''Perform the object-level necessities for promotion.'''
        PublicTraitData.promote_devel()

    def _rollback_db(self):
        '''Roll back the database transaction (use in error conditions.)'''

        transaction.rollback()
        transaction.leave_transaction_management()

    def handle(self, **options):
        '''The main entry point for the Django management command.'''

        import_start = datetime.datetime.now()
        # Start transaction management.
        transaction.commit_unless_managed()
        transaction.enter_transaction_management()
        transaction.managed(True)
        try:
            self._promote_devel()
        except:
            self._rollback_db()
            raise
        # Finalize the transaction and close the db connection.
        transaction.commit()
        transaction.leave_transaction_management()
        connection.close()
        import_end = datetime.datetime.now()

        # Print a short summary of what we did.
        td = import_end - import_start
        print '\nProcessing complete in %s days, %s.%s seconds.' % (
          td.days, td.seconds, td.microseconds)
        print '  TraitData objects promoted: %s' % (
          PublicTraitData.objects.all().count(),)
