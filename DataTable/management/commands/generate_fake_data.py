from django.core.management.base import BaseCommand
from faker import Faker
from DataTable.models import Funcionario, Cargo, Salario
import random

# Crie uma instância do Faker
fake = Faker()

class Command(BaseCommand):
    help = 'Generate and insert fake data into the database'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake records to generate')

    def delete(self):
        Salario.objects.all().delete()
        Funcionario.objects.all().delete()
        Cargo.objects.all().delete()

    def handle(self, *args, **options):
        count = options['count']

        cargos = [
            'Desenvolvedor',
            'QA',
            'TeamLider',
            'Arquiteto de Software',
            'Engenheiro de DevOps',
        ]

        # Crie um único cargo para cada tipo
        created_cargos = {}
        for cargo_nome in cargos:
            nivel = fake.random_element(elements=('Júnior', 'Pleno', 'Sênior'))
            cargo, created = Cargo.objects.get_or_create(cargo=cargo_nome, nivel=nivel)
            created_cargos[cargo_nome] = cargo

        for _ in range(count):
            # Escolha aleatoriamente um tipo de cargo
            cargo_nome = random.choice(cargos)
            cargo = created_cargos[cargo_nome]

            # Crie um funcionário com base no cargo
            funcionario = Funcionario.objects.create(
                data=fake.date_of_birth(minimum_age=18, maximum_age=65),
                nome=fake.name(),
                matricula=fake.unique.random_int(min=1000, max=9999),
                cargo=cargo,  # Associe o cargo ao funcionário
            )

            # Crie um salário para o funcionário
            salario = Salario.objects.create(
                salario=fake.pyfloat(min_value=800, max_value=4500, right_digits=2),
                funcionario=funcionario,
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully inserted {count} fake records into the database'))
