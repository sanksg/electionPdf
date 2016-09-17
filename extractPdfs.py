#http://www.ceo.kerala.gov.in/detailedResultsGE2016.html
#https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
import os
import subprocess
import re
from PyPDF2 import PdfFileWriter, PdfFileReader

csv_heading = ''',Candidate
,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U
Serial No of Polling Station,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,Total # of Valid Votes,# of Rejected,Total,# of Tend Vote
'''


csv_last_rows=[]
csv_last_rows.append("Total No of Votes recorded at Polling")
csv_last_rows.append("No.of Votes recorded on postal ballot papers(To be filled in the case of election from assembly constituency)")
csv_last_rows.append("Total Votes Polled")


tab_base_cmd = "java -jar tabula-0.9.0.jar --no-spreadsheet"
area_opt = "-a"
page_opt = "-p"


# Areas for the tabula command
area1 = "308.342,12.102,499.872,829.788" # First page
area2 = "67.351,11.05,487.244,829.788" # Normal pages between 2 to end-1
area3 = "67.351,58.563,329.389,828.735" # 1st half of last page
area4 = "355.699,11.05,385.165,838.207" # last half of last page


def get_num_pages(pdf_fn):
    pdf = PdfFileReader(open(pdf_fn, 'rb'))
    return pdf.getNumPages()


def get_pdfs(path):
    pdf_list = []
    for fn in os.listdir(path):
        match = re.findall("\d+\\.pdf", fn)
        if match:
            pdf_list.append(os.path.join(path,fn))
    if len(pdf_list) == 0:
        print ("Could not find any PDF files in the directory:",path)
    return pdf_list




def process_pdfs(pdfs, outPath):
    for pdf in pdfs:
        print(pdf)
        # Output Csv
        csvName = pdf.split('.')[0]+".csv"

        #Write the header first
        out_fh = open(csvName, "w")
        out_fh.write(csv_heading)

        # Get # pages
        pages = get_num_pages(pdf)


        #Make sure that our conversion command didn't cause an exception; if they did, skip this pdf
        conv_error = False

        #Prepare and run the cmds
        cmds = []
        #out captures the complete output
        out = ""

        # Go through a loop for each page in the pdf and the corresponding area
        for (pg, area) in zip([1,"2-"+str(pages-1)], [area1,area2]):
            #Create the tabula command by combining the base command with page + area
            cmd = " ".join([tab_base_cmd, "-p", str(pg), "-a", area, pdf])

            #Run the command and process output
            cmdOut = run_subprocess(cmd)
            #Break in case the cmd was not successful
            if cmdOut == None:
                conv_error = True
                break

            #Append the output to the out variable if successful
            out += cmdOut

        #Skip PDF if there was an error
        if conv_error:
            print("Skipping PDF ", pdf)
            break

        #Processing the last page separately since it has multiple parts
        cmdlast1 = " ".join([tab_base_cmd, "-p", str(pages), "-a", area3, pdf])

        # Try running the command and break out of loop if not successful
        last1out = run_subprocess(cmdlast1)
        if last1out == None:
            print("Skipping PDF ", pdf)
            break

        #Append the output of the last page and add row names manually
        i = 0
        for line in last1out.strip().split("\n"):
            out += csv_last_rows[i] + "," + line + "\n"
            i += 1

        #Now capture the candidate names line which is the last line on the last page
        cmdlast2 = " ".join([tab_base_cmd, "-p", str(pages), "-a", area4, pdf])
        #Run the subprocess and check if successful
        cmdlast2out = run_subprocess(cmdlast2)
        #Skip PDF if there is an error in conversion
        if cmdlast2out == None:
            print("Skipping PDF ", pdf)
            break

        #Append final line to the out variable
        out += "\n" + "," + ",".join(cmdlast2out.replace("\"","").split(","))


        # Finally, write the output to the csv file
        out_fh.write(out)



def run_subprocess(cmd):
    try:
        cmdOut = subprocess.check_output(cmd, universal_newlines=True)
    except BaseException as e:
        print("\t**=> Exception while running subprocess\nCommand:{}\nError:{}".format(pdf,cmd,str(e)))
        return None

    return cmdOut



def main():
    pdfFilesPath = "ge2011\converted"
    pdfs = get_pdfs(pdfFilesPath)
#    pdfs = [os.path.join("074.pdf")]
#    print(len(pdfs))
    process_pdfs(pdfs, pdfFilesPath);


if __name__=='__main__':
    main()
