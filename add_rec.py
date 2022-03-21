import csv
import os
import sys
import subprocess
import glob

def usage():
    print('python3 add_rec.py MANDATORY1 MANDATORY2 OPTIONAL3')
    print('MANDATORY1 : Template tex file.')
    print('MANDATORY2 : CSV file of recipient names.')
    print('OPTIONAL3  : (Optional) Generate pdf.')
    
def get_rec(csv_reclist):
    '''
    The csv file has to contain recipients in a row, with first name and last name 
    in different column.

    Parameters
    ----------
    csv_reclist : CSV file, a list of recipients. Max 2 recipients per row.

    Returns
    -------
    res2 : List of concatenated names.

    '''
    res=[]
    with open(csv_reclist) as csv_file:
        recipients = csv.reader(csv_file, delimiter=',')
        next(recipients, None)
        for row in recipients:
            res.append(row)
    res2 = []
    for i in range(len(res)):
        [res2.append(f'{res[i][j]} {res[i][j+1]}') for j in range(0,len(res[i]),2)]
    return res2

def replace_tex(texfile,rec_list):
    '''
    Replace the place holder variable {recA} and {recB} in the template tex file 
    with recipient names.

    Parameters
    ----------
    texfile : The template tex file.
    rec_list : List of concatenated names.

    Returns
    -------
    text : Substituted tex file.

    '''
    with open(texfile) as f:
        text = f.read()
    recA=rec_list[0]
    recB=rec_list[1]
    text = text.replace('{recA}', recA)
    text = text.replace('{recB}', recB)
    return text

def gen_pdf(tex_file):
    '''
    Generate pdf. Runs pdflatex twice.

    Parameters
    ----------
    tex_file : Tex file to compile.

    Returns
    -------
    x : Not sure.

    '''
    x = subprocess.call(['pdflatex', tex_file],shell=False)
    x = subprocess.call(['pdflatex', tex_file],shell=False)
    return x

def main(args):
    texfile = args[1]
    csv_reclist = args[2]
    
    #Make recipients list
    rec_list = get_rec(csv_reclist)
    
    #Make tex
    res=[]
    for i in range(0,len(rec_list),2):
        tmp_list=[rec_list[i],rec_list[i+1]]
        text=replace_tex(texfile,tmp_list)
        res.append(text)
    
    save_dir = os.path.split(texfile)[0]
    file_ext = os.path.split(texfile)[1]
    file_ext = os.path.splitext(file_ext)
    count=0
    #Write tex
    for j in res:
        complete_name = os.path.join(save_dir, f'{file_ext[0]}{rec_list[count][:4]}{file_ext[1]}')
        with open(complete_name, 'w') as tex:
            tex.write(j)
        count+=2
        print(f'Generating {complete_name}')
    
    #Generate pdf
    if len(args) == 3:
        print('Not generating pdf.')
    elif len(args)>3:
        tex_list=glob.glob(f'{os.getcwd()}/*.tex')
        for i in tex_list:
            gen_pdf(i)

    #return(result)
    
if __name__ == '__main__':
    if sys.argv[1] == '--h' or sys.argv[1] == '-h' or sys.argv[1] == 'help':
        usage()
        exit()
    else:
        main(sys.argv)
