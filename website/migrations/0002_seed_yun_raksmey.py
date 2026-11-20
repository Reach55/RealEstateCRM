from django.db import migrations


def seed_team(apps, schema_editor):
    TeamMember = apps.get_model('website', 'TeamMember')
    members = [
        ('YUN RAKSMEY', 'GENERAL MANAGER', 'team/yun-raksmey.png', 'Guiding our team with care, local insight, and a commitment to helping every client move forward with confidence.', 1),
        ('KIE SREYNY', 'SALE CONSULTANT', 'team/Kie_Sreyny.png', 'Sales Consultant | Helping you buy, sell, and invest in property with confidence.', 2),
        ('YAN SAVAT', 'SALE CONSULTANT', 'team/LGS_SAVAT1.png', 'Sales Consultant | Helping you buy, sell, and invest in property with confidence.', 2),
        ('NY MALAY', 'SALE CONSULTANT', 'team/B_LAY.png', 'Sales Consultant | Helping you buy, sell, and invest in property with confidence.', 3),
        ('DY SOPHORN', 'SALE CONSULTANT', 'team/VIP_Sophorn.png', 'Sales Consultant | Helping you buy, sell, and invest in property with confidence.', 4),
        ('SREY NICH', 'DESIGNER', 'team/IMG_2240.JPEG', 'PROFESSIONALISM IS NOT A JOB. IT’S A COMMITMENT TO EXCELLENCE.', 7),
    ]
    for name, role, photo, bio, order in members:
        TeamMember.objects.get_or_create(
            name=name,
            defaults={
                'role': role,
                'photo': photo,
                'bio': bio,
                'display_order': order,
                'is_active': True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [('website', '0001_initial')]

    operations = [migrations.RunPython(seed_team, migrations.RunPython.noop)]
