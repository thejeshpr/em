from pathlib import Path
import os
from django.core.management.base import BaseCommand, CommandError
from em.models import Transaction, Category, Account


ACCOUNTS = {
    "1": "DBS",
    "2": "Kotak Credit Card",
    "3": "Citi Credit Card",
}

class Command(BaseCommand):
    help = 'Does some magical work'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, choices=['category', 'account', 'transaction'])

    def handle(self, *args, **options):
        """ Do your work here """
        model = options.get("model")
        # self.stdout.write('There are {} things!'.format(Transaction.objects.count()))
        self.stdout.write(str(Path(__file__).resolve().parent.parent.parent.parent.parent))
        self.stdout.write(str(Path(__file__).resolve()))
        self.stdout.write(self.get_backup(options.get("model")))

    def get_backup(self, name):
        base_path = Path(__file__).resolve().parent.parent.parent.parent
        file_path = os.path.join(base_path, "backup", f"{name}.csv")
        self.stdout.write(f"Backup File: {file_path}")
        with open(f"{base_path}/backup/{name}.csv") as fd:
            return fd.read()