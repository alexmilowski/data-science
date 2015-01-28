import xml.dom.minidom;

doc = xml.dom.minidom.parseString("<doc><title>Testing</title></doc>");
title = doc.documentElement.firstChild

