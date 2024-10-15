import factory
from factory import LazyAttribute, SubFactory
from faker import Faker

from core.models import (
    Employee,
    AssesmentSkill,
    EmployeeAssesmentSkill,
    DevelopmentPlan,
    EmployeeDevelopmentPlan,
    Engagement,
    EmployeeEngagement,
    KeyPeople,
    EmployeeKeyPeople,
    TrainingApplication,
    EmployeeTrainingApplication,
    BusFactor,
    EmployeeBusFactor,
    Grade,
    EmployeeGrade,
    KeySkill,
    EmployeeKeySkill,
    Team,
    EmployeeTeam,
)
from users.models import ManagerTeam


fake = Faker('en_US')


class ManagerTeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ManagerTeam

    email = LazyAttribute(lambda _: fake.email())
    first_name = LazyAttribute(lambda _: fake.first_name())
    last_name = LazyAttribute(lambda _: fake.last_name())
    password = LazyAttribute(lambda _: fake.password())


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    slug = LazyAttribute(lambda _: fake.slug())
    team_name = LazyAttribute(lambda _: fake.company())


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    first_name = LazyAttribute(lambda _: fake.first_name())
    last_name = LazyAttribute(lambda _: fake.last_name())
    email = LazyAttribute(lambda _: fake.email())


class AssesmentSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssesmentSkill

    assesmentskill_name = LazyAttribute(lambda _: fake.word())


class EmployeeAssesmentSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeAssesmentSkill

    employee = SubFactory(EmployeeFactory)
    assesmentskill = SubFactory(AssesmentSkillFactory)
    assesment = LazyAttribute(lambda _: fake.random_int(min=0, max=100))


class DevelopmentPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DevelopmentPlan

    plan_name = LazyAttribute(lambda _: fake.word())
    employee_count = LazyAttribute(lambda _: fake.random_int(min=1, max=100))


class EmployeeDevelopmentPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeDevelopmentPlan

    employee = SubFactory(EmployeeFactory)
    development_plan = SubFactory(DevelopmentPlanFactory)
    performance_score = LazyAttribute(lambda _: fake.random_number(digits=3))
    add_date = LazyAttribute(lambda _: fake.date())


class EngagementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Engagement

    engagement_name = LazyAttribute(lambda _: fake.word())
    employee_count = LazyAttribute(lambda _: fake.random_int(min=1, max=100))


class EmployeeEngagementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeEngagement

    employee = SubFactory(EmployeeFactory)
    engagement = SubFactory(EngagementFactory)
    performance_score = LazyAttribute(
        lambda _: fake.random_int(min=1, max=100)
    )
    add_date = LazyAttribute(lambda _: fake.date())


class KeyPeopleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KeyPeople

    key_people_name = LazyAttribute(lambda _: fake.word())
    employee_count = LazyAttribute(lambda _: fake.random_int(min=1, max=100))


class EmployeeKeyPeopleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeKeyPeople

    employee = SubFactory(EmployeeFactory)
    key_people = SubFactory(KeyPeopleFactory)
    add_date = LazyAttribute(lambda _: fake.date())


class TrainingApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TrainingApplication

    training_name = LazyAttribute(lambda _: fake.word())
    employee_count = LazyAttribute(lambda _: fake.random_int(min=1, max=100))


class EmployeeTrainingApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeTrainingApplication

    employee = SubFactory(EmployeeFactory)
    training_application = SubFactory(TrainingApplicationFactory)
    add_date = LazyAttribute(lambda _: fake.date())


class BusFactorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusFactor

    bus_factor_name = LazyAttribute(lambda _: fake.word())
    employee_count = LazyAttribute(lambda _: fake.random_int(min=1, max=100))


class EmployeeBusFactorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeBusFactor

    employee = SubFactory(EmployeeFactory)
    bus_factor = SubFactory(BusFactorFactory)
    add_date = LazyAttribute(lambda _: fake.date())


class GradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Grade

    grade_name = LazyAttribute(lambda _: fake.word())


class EmployeeGradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeGrade

    employee = SubFactory(EmployeeFactory)
    grade = SubFactory(GradeFactory)


class KeySkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KeySkill

    skill_name = LazyAttribute(lambda _: fake.word())
    employee_count = LazyAttribute(lambda _: fake.random_int(min=1, max=100))


class EmployeeKeySkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeKeySkill

    employee = SubFactory(EmployeeFactory)
    key_skill = SubFactory(KeySkillFactory)
    skill_level = LazyAttribute(lambda _: fake.word())
    add_date = LazyAttribute(lambda _: fake.date())


class EmployeeTeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeTeam

    manager = SubFactory(ManagerTeamFactory)
    employee = factory.RelatedFactoryList(EmployeeFactory, 'teams', size=3)
    team = SubFactory(TeamFactory)
