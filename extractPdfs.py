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


tab_base_cmd = "java -jar tabula-0.9.1.jar --no-spreadsheet"
area_opt = "-a"
page_opt = "-p"


# Areas for the tabula command
tabulaPdfTypes = {2011: "t1", 2014: "t2", 2016: "t1"}

tabulaAreas = { "t1p1": "308.342,12.102,499.872,829.788", # First page is slightly truncated
                "t1p2": "67.351,11.05,487.244,829.788", # Normal pages between 2 to end-1
                "t1l1": "67.351,58.563,329.389,828.735", # 1st half of last page
                "t1l2": "355.699,11.05,385.165,838.207" # last half of last page
              }

                # "t2": { 'area1': "311.499,14.207,496.715,824.526",
                #         'area2': "70.508,15.259,481.982,823.474",
                #         'area3':"69.456,57.354,360.96,825.578",

numPagesArea = "507.765,29.992,528.812,146.805"


def get_num_pages(pdf_fn):
    cmd = " ".join([tab_base_cmd, "-p", str(1), "-a", numPagesArea, pdf_fn])
    cmdOut = run_subprocess(cmd)
    #Break in case the cmd was not successful
    if cmdOut == None:
        print("Error: Could not get the number of pages in file!")
        return 0
    match = re.findall("\d+", cmdOut)
    if match:
        numPages = int(match[0])
    return numPages

def get_pdfs(path):
    pdf_list = []
    for fn in os.listdir(path):
        match = re.findall("\d+\\.pdf", fn)
        if match:
            pdf_list.append(os.path.join(path,fn))
    if len(pdf_list) == 0:
        print ("Could not find any PDF files in the directory:",path)
    return pdf_list



def process_pdfs(pdfs, areas, outPath):
    for pdf in pdfs:
        print(pdf)
        # Output Csv
        csvName = pdf.split('.')[0]+".csv"

        #Write the header first
        out_fh = open(csvName, "w")
        out_fh.write(csv_heading)

        # Get total number of pages
        pages = get_num_pages(pdf)
        print(pages,"pages of tables in PDF")


        #Make sure that our conversion command didn't cause an exception; if they did, skip this pdf
        conv_error = False

        #Prepare and run the cmds
        cmds = []
        #out captures the complete output
        out = ""

        # ** NORMAL PAGES **
        # Go through a loop for each page in the pdf and the corresponding area
        for (pg, area) in zip([1,"2-"+str(pages-1)], [areas['t1p1'], areas['t1p2']]):
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

        # ** LAST PAGE - PART 1 **
        #Processing the last page separately since it has multiple parts
        totalsPagePollingVotes = " ".join([tab_base_cmd, "-p", str(pages), "-a", areas['t1l1'], pdf])

        # Try running the command and break out of loop if not successful
        totalsPagePollingVotes_out = run_subprocess(totalsPagePollingVotes)
        if totalsPagePollingVotes_out == None:
            print("Skipping PDF ", pdf)
            break

        #Append the output of the last page and add row names manually
        # The last page looks like this
        #   Total No of Votes recorded at Polling 1107 11207 51226 56922 602 88 768 2537 74 254 91 268 454 192 90 698 0 0 0 0 989 126578 0 126578 1
        #   No.of Votes recorded on postal ballot papers
        #   Total Votes Polled 1107 11207 51226 56922 602 88 768 2537 74 254 91 268 454 192 90 698 0 0 0 0 989
        #
        # If the 2nd row is empty, there is a mismatch in the rownames and the
        # values to be put there (3 vs 2). So we need to insert a 0 in the data
        # values list, if the lastPageData is 1 less than the csv_last_rows.

        i = 0
        lastPageData = totalsPagePollingVotes_out.strip().split("\n")
        if len(lastPageData) == len(csv_last_rows) - 1:
            lastPageData.insert(1,"0")
        # Go through the data lines, append them with the row names, and add them
        # to the output
        for line in lastPageData:
            out += csv_last_rows[i] + "," + line + "\n"
            i += 1

        # ** LAST PAGE - PART 2 **
        #Now capture the candidate names line which is the last line on the last page
        #There are 2 cases for the 2 types of files. The operations are the same,
        #so we'll just put a loop here
        for ind in range(0,0):
            key = "area" + str(ind)
            if key in areas:
                cmdlast2 = " ".join([tab_base_cmd, "-p", str(pages), "-a", areas[key], pdf])
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
    pdfFilesPath = "ge2014"
    pdfs = get_pdfs(pdfFilesPath)
#    pdfs = [os.path.join("074.pdf")]
    process_pdfs(pdfs, tabulaAreas, pdfFilesPath);


if __name__=='__main__':
    main()
