import os
import numpy as np
import pandas as pd


def get_pdf_list(path):
    pdf_list = []
    for fn in os.listdir(path):
        match = re.findall("\d+\\.pdf", fn)
        if match:
            pdf_list.append(os.path.join(path,fn))
    if len(pdf_list) == 0:
        print ("Could not find any PDF files in the directory:",path)
    return pdf_list


def wrangle_results(results_fn):
    # Prepare the 2016 Results file
    df = pd.read_csv("lacResults2016.csv")
    df.drop(df.columns[0], axis=1, inplace=True)

    newcols1 = ['Constituency', 'District', 'Candidate', 'Party', 'Votes']
    part1 = df.iloc[:,0:5]
    part1.columns = newcols1
    newcols2 = newcols1[2:5]
    part2 = df.iloc[:,5:8]
    part2.columns = newcols2
    part3 = df.iloc[:,8:11]
    part3.columns = newcols2

    comp = pd.concat([part1, part2, part3], axis=0)
    comp.reset_index(inplace=True)
    comp.drop('index', axis=1, inplace=True)
    comp['Alliance'] = pd.DataFrame(['UDF']*140 + ['LDF']*140 + ['NDA']*140)
    comp['Constituency'] = pd.concat([comp.iloc[0:140,1]] * 3).tolist()
    comp['District'] = pd.concat([comp.iloc[0:140,2]] * 3).tolist()
    comp['Votes'] = comp['Votes'].apply(pd.to_numeric, errors = 'coerce')





def get_main_cands(fileList, resultsFrame):
    finalFrame = pd.DataFrame(columns=)
    for fn in fileList:
        # Now go through each constituency file and look up the candidate names from the results file
        const1 = pd.read_csv(fn, skiprows=[0,1])
        const1.drop([170], axis=0, inplace=True)
        const1[const1.columns[1:22]] = const1[const1.columns[1:22]].apply(pd.to_numeric, errors='coerce')
        c1 = const1.transpose()
        c1.columns = c1.iloc[0,:]
        c1.drop(c1.index[0], axis=0, inplace=True)
        c1.columns.name=None
        c1 = c1.apply(pd.to_numeric, errors = 'coerce')

        results = pd.merge(c1, comp, left_on="Total Votes Polled", right_on='Votes', how='inner', suffixes=('_x', '')).dropna(axis=1)
        finalFrame = pd.concat([finalFrame, results], axis = 0)


def main():
    pdfFilesPath = "ge2014"
    filesPath = '../electionPdf/ge2016/csvs/001.csv'

    pdfs = get_pdf_list(pdfFilesPath)
#    pdfs = [os.path.join("074.pdf")]
    process_pdfs(pdfs, tabulaAreas, pdfFilesPath);


if __name__=='__main__':
    main()
