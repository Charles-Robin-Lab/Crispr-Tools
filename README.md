# Crispr Tools
 A script to merge exported results from CRISPRdirect(as a json file) with those from CHOP CHOP(as a tsv file) in order to find the best guideRNA!
 Due to limitations in CRISPRdirect with larger genes, multiple exported CRISPRdirect files can be specified when running this tool.  
 Example usage:
 ```sh
 py gRNA_designer.py --crisprdirect 'examples/1-1CRISPRdirect.json' 'examples/1-2CRISPRdirect.json' 'examples/1-3CRISPRdirect.json' 'examples/1-4CRISPRdirect.json' --chop 'examples/2results.tsv' --out examples/out.csv 
 ```