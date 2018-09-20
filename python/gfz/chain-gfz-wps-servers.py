from owslib.wps import WebProcessingService

wps = WebProcessingService('https://riesgos.52north.org/wps/WebProcessingService', verbose=False, skip_caps=True)

processid = 'org.n52.wps.python.algorithm.QuakeMLProcess'
inputs = [ ("lonmin","288"),
           ("lonmax", "292"),
           ("latmin", "-70"),
           ("latmax","-10"),
           ("mmin","6.6"),
           ("mmax","8.5"),
           ("zmin","5"),
           ("zmax","140"),
           ("p","0.1"),
           ("etype","deaggregation"),
           ("tlon","-71.5730623712764"),
           ("tlat","-33.1299174879672")
          ]
output = "selected-rows"
execution = wps.execute(processid, inputs, output)

from owslib.wps import monitorExecution
monitorExecution(execution)

print(execution.processOutputs[0].reference)

from owslib.wps import ComplexDataInput
quakeMLInput = ComplexDataInput(value = execution.processOutputs[0].reference)

quakeMLInput.schema = "http://quakeml.org/xmlns/quakeml/1.2/QuakeML-1.2.xsd"
quakeMLInput.mimeType = "text/xml"

processid2 = 'org.n52.wps.python.algorithm.ShakemapProcess'
inputs2 = [ ("quakeml-input", quakeMLInput)]
output2 = "shakemap-output"
execution2 = wps.execute(processid2, inputs2, output2)

monitorExecution(execution2)

print(execution2.processOutputs[0].reference)

import urllib.request
contents = urllib.request.urlopen(execution2.processOutputs[0].reference).read()

output_file = open("shakemap-output.xml", "w")
output_file.write(contents.decode("utf-8"))
output_file.close()

