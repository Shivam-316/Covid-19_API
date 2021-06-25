from django.db import models

class StatewiseData(models.Model):
    date = models.DateField()
    state = models.CharField(max_length=255)
    key = models.CharField(max_length=3)
    confirmed = models.PositiveBigIntegerField(default=0,null=True,blank=True)
    recovered = models.PositiveBigIntegerField(default=0,null=True,blank=True)
    deceased = models.PositiveBigIntegerField(default=0,null=True,blank=True)
    first_dose = models.PositiveBigIntegerField(verbose_name='First Dose Administered',default=0,null=True,blank=True)
    second_dose = models.PositiveBigIntegerField(verbose_name='Second Dose Administered',default=0,null=True,blank=True)
    male_vcc = models.PositiveBigIntegerField(verbose_name='Male Vaccinated',default=0,null=True,blank=True)
    female_vcc = models.PositiveBigIntegerField(verbose_name='Female Vaccinated',default=0,null=True,blank=True)
    transgender_vcc = models.PositiveBigIntegerField(verbose_name='Transgender Vaccinated',default=0,null=True,blank=True)
    total_covishield = models.PositiveBigIntegerField(verbose_name='Total Covishield Administered',default=0,null=True,blank=True)
    total_covaxin = models.PositiveBigIntegerField(verbose_name='Total Covaxin Administered',default=0,null=True,blank=True)
    total_sputnik =  models.PositiveBigIntegerField(verbose_name='Total Sputink V Administered',default=0,null=True,blank=True)
    age18_45 = models.PositiveBigIntegerField(verbose_name='18-45 Age Administered',default=0,null=True,blank=True)
    age45_60 = models.PositiveBigIntegerField(verbose_name='45-60 Age Administered',default=0,null=True,blank=True)
    age60 = models.PositiveBigIntegerField(verbose_name='60+ Age Administered',default=0,null=True,blank=True)

    def __str__(self):
        return f"{self.state} on {self.date}"


