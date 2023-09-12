from django.core.management.base import BaseCommand
from faker import Faker
from DataTable.models import Funcionario

# Crie uma instância do Faker
fake = Faker()

class Command(BaseCommand):
    help = 'Generate and insert fake data into the database'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake records to generate')

    def delete(self):
        Funcionario.objects.all().delete()

    def handle(self, *args, **options):
        count = options['count']

        for _ in range(count):
            Funcionario.objects.create(
                data=fake.date_of_birth(minimum_age=18, maximum_age=65),
                nome=fake.name(),
                matricula=fake.unique.random_int(min=1000, max=9999),
                cargo=fake.job(),
                nivel=fake.random_element(elements=('Júnior', 'Pleno', 'Sênior')),
                valor_base=fake.random_int(min=2000, max=10000),
                proventos=fake.pyfloat(min_value=1000, max_value=5000, right_digits=2),
                descontos=fake.random_int(min=100, max=1000),
                liquidos=fake.pyfloat(min_value=800, max_value=4500, right_digits=2)
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully inserted {count} fake records into the database'))