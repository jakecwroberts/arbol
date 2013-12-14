from django.db import models

class Section(models.Model):
    '''
    A Section is a grouping of students.
    '''
    name         = models.CharField(max_length="20")
    abbreviation = models.SlugField()

    def __unicode__(self):
        return self.name

class Student(models.Model):
    '''
    A Student is a student enrolled in this class.
    '''
    first_name  = models.CharField(max_length="30")
    middle_name = models.CharField(max_length="50", blank=True)
    last_name   = models.CharField(max_length="30")

    student_number = models.CharField(max_length="20", unique=True)
    netid          = models.CharField(max_length="20", unique=True)
    
    section     = models.ForeignKey(Section, blank=True, null=True, 
                                  related_name="students")

    class Meta:
        ordering = ['last_name', 'first_name']    

    def full_name(self):
        '''
        Returns the full name of this student.
        '''
        if self.middle_name:
            mid = " " + self.middle_name + " "
        else:
            mid = " "
        return self.first_name + mid + self.last_name

    def __unicode__(self):
        return self.full_name()
