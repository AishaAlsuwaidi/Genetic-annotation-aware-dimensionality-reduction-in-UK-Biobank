# Genetic-annotation-aware-dimensionality-reduction-in-UK-Biobank
To run these files and generate the results download all files in zip formant.
The below figure represents the workflow of the bash scripts. The start script is Samples.exec.
![bash workflow](https://user-images.githubusercontent.com/71970449/166122307-3e457638-f35d-4596-b8e9-7da1d3e837c6.png)

A discription of the scripts:
1. Samples.exec: read file codes.txt, get a single diseases name and its ICD code. Execute Samples_run, then generate a text file of the names of the diseases.
2. Samples_run.exec: using the ICD codes and a python script (generate_samples.py) generate cases and controls files.
  a. Run downsample.py python file which down sample the number of cases and controls, it also parses the SNPs XML file into a text files.
3. plinky.exec: read diseases.txt file line by line, then for each line run plinky_run.exec
4. plinky_run.exec: generate plink files for the input disease name.
