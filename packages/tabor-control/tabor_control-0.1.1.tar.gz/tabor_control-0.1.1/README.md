# tabor_control

This package provides a thin abstraction over SCPI controlled Tabor Electronics AWGs.

 - Discovery of such devices in the networkl 
 - Initialization of visa sessions with reasonable defaults
 - Binary up- and download of waveform segments and sequencing tables
 - Device properties like total memory and sequence restrictions
 - Workaround some quirks if a simulator is used
 - Basic object-oriented interface to the above
