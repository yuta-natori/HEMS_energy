# -*- coding: utf-8 -*-
from django import forms

CHOICE_YEARS = (
    (None, "-"),
    (1998, 1998),
    (1999, 1999),
    (2000, 2000),
    (2001, 2001),
    (2002, 2002),
    (2003, 2003),
    (2004, 2004),
    (2005, 2005),
    (2006, 2006),
    (2007, 2007),
    (2008, 2008),
    (2009, 2009),
    (2010, 2010),
    (2011, 2011),
    (2012, 2012),
    (2013, 2013),
    (2014, 2014),
    (2015, 2015),
    (2016, 2016),
    (2017, 2017),
    (2018, 2018),
    (2019, 2019),
    (2020, 2020)
)

CHOICE_MONTH = (
    (None, "-"),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11),
    (12, 12)
)

CHOICE_WEEK = (
    (None, "-"),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4)
)

class TrendAnalysisFormClass(forms.Form):
    area = forms.CharField(
        label='地域の指定',
        max_length=50,
        required=True,
    )