#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygal
import os

line_chart = pygal.StackedLine(fill=True)
line_chart.title = 'Browser usage evolution (in %)'
#line_chart.x_labels = ['2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012']
line_chart.x_labels = map(str,range(2002,2013))
line_chart.add('Firefox',[None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
line_chart.add('Chrome',[None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
line_chart.add('IE',[85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
line_chart.add('Others',[14.2, 15.4, 15.3,  8.9, 9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
line_chart.render()

#f=open('aab.html','w')
#f.write(line_chart.render())
#f.close()

worldmap_chart = pygal.Worldmap()
worldmap_chart.title = 'Some countries'
worldmap_chart.add('F countries',['fr','fi'])
worldmap_chart.add('M countries',['ma','mc','md','me','mg','mk','ml','mm','mn','mo','mr','mt'])
worldmap_chart.add('U countries',['ua','ug','us','uy','uz'])
worldmap_chart.add('C contries',['cn','ch','ca','ca'])
worldmap_chart.render()

wf=open('world.html','w')
f.write(worldmap_chart.render())
f.close()
