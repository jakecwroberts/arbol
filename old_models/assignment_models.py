from django.db import models
from students.models import *

UNPACK_ROOT = "../student_files"

class Assignment(models.Model):
    '''
    Represents an assignment for a class.
    '''
    name          = models.CharField(max_length=20)
    abbreviation  = models.SlugField()

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.abbreviation)


class Submission(models.Model):
    '''
    Represents an assignment turned in by a student
    '''
    student = models.ForeignKey(Student, related_name = "submissions")
    assignment = models.ForeignKey(Assignment, related_name="submissions")
    
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return"%s - %s" % (self.assignment, self.student)


class SubmissionFile(models.Model):
    '''
    Represents a single file of a Submission
    '''
    submission = models.ForeignKey(Submission, related_name="files")
    
    file_path = models.FilePathField(path=UNPACK_ROOT, recursive=True)

    def content(self):
        '''
        Returns the content of this file as a string.
        '''
        file = open(self.file_path, 'r')
        return file.read()
    
    def lines(self):
        '''
        Returns the contents of this file as a list of lines.
        '''
        file = open(self.file_path, 'r')
        return file.readlines()

    def filename(self):
        '''
        Returns the filename of this file.
        '''

    def __unicode__(self):
        return "%s %s" % (self.submission.__unicode__(), self.filename())

COLORS = (
  ("Y", "Yellow"),
	("R", "Red"),
	("G", "Green"),
	("B", "Blue"),
	)

class Note(models.Model):
    '''
    A note made on a submitted file.
    '''
    file = models.ForeignKey(SubmissionFile, related_name="notes")

    title = models.CharField(max_length=50)
    text = models.TextField()
    color = models.CharField(max_length=1, choices=COLORS)
    line = models.PositiveIntegerField()

    class Meta:
        ordering=['line']

class Highlight(models.Model):
    '''
    A highlighted region of text in a submitted file.
    '''
    file = models.ForeignKey(SubmissionFile, related_name="highlights")

    color = models.CharField(max_length=1, choices=COLORS)
    line = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    width = models.PositiveIntegerField()

    class Meta:
        ordering=['line', 'column', 'width']
